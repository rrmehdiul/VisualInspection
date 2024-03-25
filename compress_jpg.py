import os
import cv2
import imghdr
"""
Compress the images as they are too large (> 1.5Mb limit)
"""

input_folder = "./JPEG/" # the folder with jpg images to compress
output_folder = "./compressed_images/"
img_target_size = (1500, 1500)

#-----------------------------------------------------------------------

# Create the output folder
os.makedirs(output_folder, exist_ok=True)

# Iterate over the image files in the input folder
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)

    # check if the file is an image?
    if imghdr.what(file_path) is None:
       continue
       
    # Read the image
    image = cv2.imread(file_path)
       
    height, width, _ = image.shape
    #print("orig shape ", image.shape)
    max_dimension = max(height, width)
    scale_factor = 1500/max_dimension
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    #print("new shape", (new_width, new_height))
       
    # Resize the image to NxN pixels
    resized_image = cv2.resize(image, (new_width, new_height), img_target_size)

    # Save the converted image
    output_path = os.path.join(output_folder, file_name)
    cv2.imwrite(output_path, resized_image)

