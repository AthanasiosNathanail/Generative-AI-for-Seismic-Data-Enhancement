from PIL import Image
import os

# Function to split and save images
def split_image(image_path):
    # Load the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Check if the image has the expected dimensions
    if img_width != 3072 or img_height != 768:
        print(f"Image {image_path} does not have the expected dimensions of 3072x768.")
        return

    # Extract the base name of the image without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Split the image into four parts
    for i in range(4):
        left = i * 768
        right = (i + 1) * 768
        cropped_img = img.crop((left, 0, right, 768))
        new_image_name = f"{base_name}{chr(97 + i)}.png"  # chr(97) is 'a', chr(98) is 'b', etc.
        cropped_img.save(os.path.join(output_dir, new_image_name))
        print(f"Saved {new_image_name}")

# Directory containing the images
input_dir = "C:/Users/your path/Results/BW - Segmented"
output_dir = "C:/Users/your path/Results/BW_final"


# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each image in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".png"):
        split_image(os.path.join(input_dir, filename))
