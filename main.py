# import Craft class
from craft_text_detector import Craft
import cv2
# import numpy as np
import pytesseract
# from PIL import Image
# from pytesseract import image_to_string
import os

# Path of working folder on Disk Replace with your working folder
# src_path = ".\\outputs\\"
# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'

# set image path and export folder directory
image = 'im001.png' # can be filepath, PIL image or numpy array
output_dir = 'outputs/'

# folder path
# dir_path = r'.\\outputs\\'
dir_path = '.\\outputs\\' + image[:-4] + '_crops' + '\\'
src_path = '.\\outputs\\' + image[:-4] + '_crops' + '\\'
dir_path_rev = '.\\outputs_rev\\'

# create a craft instance
craft = Craft(output_dir=output_dir, crop_type="poly", cuda=False)

# apply craft text detection and export detected regions to output directory
prediction_result = craft.detect_text(image)

# unload models from ram/gpu
craft.unload_craftnet_model()
craft.unload_refinenet_model()

filepath = '.\\outputs\\' + image[:-4] + '_text_detection.txt'
text_detect_path = '.\\outputs\\' + image[:-4] + '_crops_corrected' + '\\'
image = cv2.imread(image)

# removing the new line characters
with open(filepath) as f:
    lines = [line.rstrip() for line in f]
# print(lines)


i = 0
for line in lines:
    if line:
        numbs = line.split(',')
        crop_image = image[int(int(numbs[1])*0.99):int(int(numbs[5])*1.01), int(int(numbs[0])*0.99):int(int(numbs[2])*1.01)]
        # cv2.imshow("Cropped", crop_image)
        cropname = 'crop_' + str(i) + '.png'
        path = '.\\outputs_rev\\' + cropname
        i += 1
        cv2.imwrite(path, crop_image)

# list to store files
all_bondboxes = []

# Iterate directory
for path in os.listdir(dir_path_rev):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path_rev, path)):
        all_bondboxes.append(path)
# print(all_bondboxes)

config = r'--oem 3 --psm 6'
print('--- Start recognize text from image ---')

for boundbox in all_bondboxes:
    img_cv = cv2.imread(dir_path_rev + boundbox)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img_rgb, config=config))

print("------ Done -------")
