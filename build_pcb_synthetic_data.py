"""
Copyright: AILab
"""
import os
from PIL import Image
import cv2
#"""
#Script to split images to create synthetic PCB data
#"""
# set working folders
# an input folder with images to work with
images_folder = os.listdir("./bare_boards/templates/")

# an output folder for image files created in this script
OUTPUT_FOLDER = 'new_background'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

IMAGE_COUNTER = 0

CURRENT_FOLDER = "./"
pngs = os.listdir(CURRENT_FOLDER)

for item in pngs:
    if item.endswith(".png"):
        os.remove( os.path.join(CURRENT_FOLDER, item))

# split PCB images to subparts
for file in images_folder:
    if (file.endswith(".jpg") or file.endswith(".png")):
        #print("read file ==> ", file)
        image = Image.open("./bare_boards/templates/"+str(file))
        image1 = cv2.imread("./bare_boards/templates/"+str(file))
        height, width, _ = image1.shape

        max_dim = max(height, width)
        scale_factor = 2048/max_dim
        img_target_size = (2048, 2048)

        # scaling images up
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)

        # resize the image to calculated NxN pixels
        resized_image = cv2.resize(image1, (new_width, new_height), img_target_size)
        cv2.imwrite("./temp_resized.png", resized_image)

        # new image output size
        part_height, part_width = 512, 512

        resized_image = Image.open('./temp_resized.png')

        # calculate rows and columns for the image grid
        num_cols = resized_image.width // part_width
        num_rows = resized_image.height // part_height

        # split the image into smaller parts
        for row in range(num_rows):
            for col in range(num_cols):
                # define the coordinates of each part
                top = row * part_height
                bottom = top + part_height
                left = col * part_width
                right = left + part_width

                # crop and save each part in png format
                part = resized_image.crop((left, top, right, bottom))
                part.save(f'part_{row}_{col}.png')

        new_pngs = os.listdir('./')
        for png_file in new_pngs:
            if png_file.startswith('part') and png_file.endswith('.png'):
                IMAGE_COUNTER = IMAGE_COUNTER + 1
                extension = png_file.split('.')[-1]
                new_filename = f'{IMAGE_COUNTER}.{extension}'
                old_filepath = os.path.join("./",png_file)
                new_filepath = os.path.join(OUTPUT_FOLDER,new_filename)
                os.rename(old_filepath, new_filepath)
        # final count of the generated PNG files
        FINAL_COUNT = IMAGE_COUNTER
print("final_count of created background images", FINAL_COUNT)
