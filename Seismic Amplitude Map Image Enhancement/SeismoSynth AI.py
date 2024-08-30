
import streamlit as st
from PIL import Image
import numpy as np
import torch
from omegaconf import OmegaConf
import math
# Ensure these utilities are correctly imported
from utils.image import auto_resize, pad
# Ensure these are correctly imported
from model.spaced_sampler import SpacedSampler
from model.cldm import ControlLDM
from utils.common import instantiate_from_config, load_state_dict
import pytorch_lightning as pl
# Ensure this is correctly imported
from ldm.xformers_state import disable_xformers
from tqdm import tqdm
import einops

# Assuming the configuration is also hardcoded or available as a file
config_path = 'configs/model/cldm.yaml'  # Update this path to your actual config file location
ckpt_path = 'weights/general_full_seismic.ckpt'  # Path to the trained model checkpoint

device_selection = "cuda" if torch.cuda.is_available() else "cpu"  # Automatically select device based on availability

# Function to load the model (adapt this to match how your model is initialized and loaded)

@st.cache(allow_output_mutation=True)
# @st.cache_resource
def load_model(config_path, ckpt_path, device="cuda"):
    config = OmegaConf.load(config_path)
    model = instantiate_from_config(config)  # instantiate_from_config should be defined or imported
    load_state_dict(model, torch.load(ckpt_path, map_location=device), strict=True)  # load_state_dict should be defined or imported
    model.freeze()
    model.to(device)
    sampler = SpacedSampler(model, var_type="fixed_small")  # SpacedSampler should be defined or imported
    return model, sampler

model, sampler = load_model(config_path, ckpt_path, device_selection)

@torch.no_grad()
def process_image(control_img, num_samples, sr_scale, disable_preprocess_model,
                  strength, positive_prompt, negative_prompt, cfg_scale, steps,
                  use_color_fix, seed, tiled, tile_size, tile_stride):
    pl.seed_everything(seed)
    if sr_scale != 1:
        control_img = control_img.resize((math.ceil(x * sr_scale) for x in control_img.size), Image.BICUBIC)
    input_size = control_img.size
    if not tiled:
        control_img = auto_resize(control_img, 512)
    else:
        control_img = auto_resize(control_img, tile_size)
    h, w = control_img.height, control_img.width
    control_img = pad(np.array(control_img), scale=64)
    control = torch.tensor(control_img[None] / 255.0, dtype=torch.float32, device=model.device).clamp_(0, 1)
    control = einops.rearrange(control, "n h w c -> n c h w").contiguous()
    if not disable_preprocess_model:
        control = model.preprocess_model(control)
    height, width = control.size(-2), control.size(-1)
    model.control_scales = [strength] * 13
    preds = []
    for _ in tqdm(range(num_samples), leave=False):
        shape = (1, 4, height // 8, width // 8)
        x_T = torch.randn(shape, device=model.device, dtype=torch.float32)
        if not tiled:
            samples = sampler.sample(steps=steps, shape=shape, cond_img=control,
                                     positive_prompt=positive_prompt, negative_prompt=negative_prompt, x_T=x_T,
                                     cfg_scale=cfg_scale, cond_fn=None,
                                     color_fix_type="wavelet" if use_color_fix else "none")
        else:
            samples = sampler.sample_with_mixdiff(tile_size=tile_size, tile_stride=tile_stride,
                                                  steps=steps, shape=shape, cond_img=control,
                                                  positive_prompt=positive_prompt, negative_prompt=negative_prompt, x_T=x_T,
                                                  cfg_scale=cfg_scale, cond_fn=None,
                                                  color_fix_type="wavelet" if use_color_fix else "none")
        x_samples = samples.clamp(0, 1)
        x_samples = (einops.rearrange(x_samples, "b c h w -> b h w c") * 255).cpu().numpy().astype(np.uint8)
        img = Image.fromarray(x_samples[0, :h, :w, :]).resize(input_size, Image.LANCZOS)
        preds.append(np.array(img))
    return preds

# Streamlit UI
st.title("SeismoSynth AI")

control_img = st.file_uploader("Upload Control Image", type=["png", "jpg", "jpeg"])
num_samples = st.slider("Number Of Samples", 1, 12, 1)
sr_scale = st.number_input("SR Scale", value=1)
disable_preprocess_model = st.checkbox("Disable Preprocess Model", value=False)
strength = st.slider("Control Strength", 0.0, 2.0, 1.0, 0.01)
positive_prompt = st.text_input("Positive Prompt")
negative_prompt = st.text_area("Negative Prompt", value="longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality")
cfg_scale = st.slider("Classifier Free Guidance Scale", 0.1, 30.0, 1.0, 0.1)
steps = st.slider("Steps", 1, 100, 50)
use_color_fix = st.checkbox("Use Color Correction", value=True)
seed = st.number_input("Seed", -1, 2147483647, 231)
tiled = st.checkbox("Tiled", value=False)
tile_size = st.slider("Tile Size", 512, 1024, 512, 256)
tile_stride = st.slider("Tile Stride", 256, 512, 256, 128)

if st.button("Process Image") and control_img is not None:
    control_img_pil = Image.open(control_img).convert("RGB")
    processed_images = process_image(control_img_pil, num_samples, sr_scale, disable_preprocess_model,
                                      strength, positive_prompt, negative_prompt, cfg_scale, steps,
                                      use_color_fix, seed, tiled, tile_size, tile_stride)
    for img_array in processed_images:
        st.image(img_array, use_column_width=True)
else:
    st.write("Please upload an image and configure options to process.")