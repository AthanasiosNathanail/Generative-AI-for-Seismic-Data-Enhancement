import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

def calculate_metrics(original_img_path, upscaled_img_path):
    # Load images
    original = cv2.imread(original_img_path, cv2.IMREAD_COLOR)
    upscaled = cv2.imread(upscaled_img_path, cv2.IMREAD_COLOR)

    # Resize original image to match the upscaled image's dimensions
    resized_original = cv2.resize(original, (upscaled.shape[1], upscaled.shape[0]))

    # Convert images to grayscale for SSIM calculation
    original_gray = cv2.cvtColor(resized_original, cv2.COLOR_BGR2GRAY)
    upscaled_gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)

    # Calculate PSNR, MSE, and SSIM
    psnr_value = psnr(resized_original, upscaled, data_range=upscaled.max() - upscaled.min())
    mse_value = mse(resized_original, upscaled)
    ssim_value, _ = ssim(original_gray, upscaled_gray, full=True)

    # Placeholder for FSIM and MS-SSIM - you need to define or install a library for these metrics
    fsim_value = "Not implemented"
    ms_ssim_value = "Not implemented"

    return {
        "PSNR": psnr_value,
        "MSE": mse_value,
        "SSIM": ssim_value,
        "FSIM": fsim_value,
        "MS-SSIM": ms_ssim_value
    }

# Example usage
original_path = "C:/Users/athos/Documents/SMART Project/SMART EY23 Submission/Task 4.4.2/Data/test/seismic.jpg"
upscaled_path = "C:/Users/athos/Documents/SMART Project/SMART EY23 Submission/Task 4.4.2/Source code/results/demo/general/seismic_upscaled(a).jpg"
metrics = calculate_metrics(original_path, upscaled_path)
print("Evaluation Metrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
