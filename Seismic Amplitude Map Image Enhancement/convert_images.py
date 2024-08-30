import os
from skimage import io
from PIL import Image

def convert_images(input_folder, output_folder):
    # Create output folders if they do not exist
    png_output_folder = os.path.join(output_folder, "PNG")
    jpg_output_folder = os.path.join(output_folder, "JPG")

    if not os.path.exists(png_output_folder):
        os.makedirs(png_output_folder)
    if not os.path.exists(jpg_output_folder):
        os.makedirs(jpg_output_folder)

    # Get list of TIFF images
    file_list = [f for f in os.listdir(input_folder) if f.endswith(".tiff")]

    for filename in file_list:
        file_path = os.path.join(input_folder, filename)
        
        # Load the image
        image = io.imread(file_path)

        # Convert and save as PNG
        png_filename = os.path.splitext(filename)[0] + ".png"
        png_file_path = os.path.join(png_output_folder, png_filename)
        io.imsave(png_file_path, image)
        
        # Convert and save as JPG
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_file_path = os.path.join(jpg_output_folder, jpg_filename)
        image_pil = Image.fromarray(image)
        image_pil.save(jpg_file_path)

        print(f"Converted and saved: {filename} as PNG and JPG")

def main():
    input_folder = "C:/Users/athos/Documents/GenAI Seismic Publication/Seismic Image Enhancement/Mathias Tiffs/"
    output_folder = "C:/Users/athos/Documents/GenAI Seismic Publication/Seismic Image Enhancement/Mathias Tiffs/Upscaled/"
    
    convert_images(input_folder, output_folder)

if __name__ == "__main__":
    main()
