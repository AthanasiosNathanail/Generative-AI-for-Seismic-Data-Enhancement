# Generative AI for Seismic Data Enhancement
 A novel workflow for fine-tuning Stable Diffusion Models for domain-specific applications

# Overview
This research explores the use of generative AI, specifically the state-of-the-art Stable Diffusion model, to generate and enhance 2D images of seismic amplitude maps. Seismic imaging plays a vital role in geosciences, particularly for evaluating subsurface structures and assessing the potential for carbon capture and storage (CCS). However, obtaining high-resolution seismic data is often expensive and logistically challenging, especially in regions where data is scarce or unavailable.

To overcome these challenges, we propose a novel workflow that utilizes generative AI to produce and enhance synthetic images of seismic amplitude maps using existing analog data. This method not only facilitates the generation of new seismic images in data-limited areas but also improves the resolution of existing images by creating high-quality representations from a compact latent space. Our cost-effective and efficient approach aims to enhance the accuracy of subsurface characterizations and enable more informed decision-making in carbon capture and storage efforts.

# Keywords
CCS
Stable Diffusion
Seismic Amplitude Maps
Geophysics
Generative AI
Seismic Imaging
Image Resolution
Super Resolution
Geophysical Image Processing
Image Denoising
Seismic_Amplitude_Maps_Finetuning_Stable_Diffusion

# Methodology
The methodology outlined in this manuscript involves a three-step workflow:

Data Preparation: A 3D seismic volume is selected from the chosen dataset and then sliced along different xlines, inlines, and time slices to create a synthetic image dataset. This dataset consists of various amplitude maps that capture different aspects of the seismic data.

Model Training: The synthetic image dataset is used to train and fine-tune a pre-trained Stable Diffusion model. This model learns to accurately generate new seismic amplitude maps, effectively capturing the characteristics of the original seismic data.

Resolution Enhancement: In the final step, a second Stable Diffusion model is trained and fine-tuned using the previously generated synthetic amplitude maps. This model focuses on learning to enhance the resolution of seismic images, thereby improving the clarity and detail of the generated amplitude maps.

# The paper presenting all this work is currently submitted and under review.

# Useful links

Please find the link to the Icthys dataset: https://terranubis.com/datainfo/FORCE-ML-Competition-2020

Please find the link to the synthetic Image Generation model's weights: https://drive.google.com/drive/folders/1_4ZzZh_CZpiGEagKtrcg8-KYRbaA7V_3

Please find the link to the Image Enhancement model's weights: https://www.dropbox.com/scl/fi/gy17d5tq2z7ziaeguh3fz/general_full_seismic.ckpt?rlkey=k6vrga22cdz356nwlyb73mgix&st=1t57pa2b&dl=0



