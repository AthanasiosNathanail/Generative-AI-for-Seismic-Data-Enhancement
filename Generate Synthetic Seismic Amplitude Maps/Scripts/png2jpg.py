
import cv2, os


def png_to_jpeg_converter(filePath):
    base_path = filePath
    new_path = filePath
    for infile in os.listdir(base_path):
        # print("file : " + infile)
        read = cv2.imread(base_path + infile)
        outfile = infile.split('.')[0] + '.jpg'
        cv2.imwrite(new_path + outfile, read, [int(cv2.IMWRITE_JPEG_QUALITY), 200])
        # Deleting the .tiff file after converting
        if infile[-3:] == "png":
            print(infile)
            os.remove(filePath + '/' + infile)
            # check if file exists or not


if __name__ == "__main__":
    print("cleaning the files")
    png_to_jpeg_converter("C:/Users/your path/")