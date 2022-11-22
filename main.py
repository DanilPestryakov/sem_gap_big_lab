import cv2
# Import Craft class for text detection
from craft_text_detector import Craft
import pytesseract
import numpy as np
import os
import shutil
import re

# In WINDOWS only. If you don't have tesseract executable in your PATH, include the following
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# set an image
image = 'im001.png' # can be filepath, PIL image or numpy array
pattern = re.search('(.+?).png', image).group(1)

# Create all paths needed
# path to automatically detected Craft text pieces
auto_text_dir = os.path.join('outputs')
# path to text pieces with expanded boundboxes for better recognition
expanded_text_dir = os.path.join('outputs_rev')
# path to file with text boundboxes coordinates
text_coords_dir = os.path.join('outputs', pattern + '_text_detection.txt')

# Cleaning folders if not empty
if os.path.exists(auto_text_dir):
    if os.listdir(auto_text_dir):
        shutil.rmtree(auto_text_dir, ignore_errors=False, onerror=None)

if os.path.exists(expanded_text_dir):
    if os.listdir(expanded_text_dir):
        shutil.rmtree(expanded_text_dir, ignore_errors=False, onerror=None)

# Check if folders exist, creating if they do not
if not os.path.exists(auto_text_dir): os.makedirs(auto_text_dir)
if not os.path.exists(expanded_text_dir): os.makedirs(expanded_text_dir)

# create a craft instance
craft = Craft(output_dir=auto_text_dir, crop_type="poly", cuda=False)
# apply craft text detection and export detected regions to output directory
prediction_result = craft.detect_text(image)
# unload models from ram/gpu
craft.unload_craftnet_model()
craft.unload_refinenet_model()

# reading the image
image = cv2.imread(image)

# reading text coordinates, removing the new line characters
with open(text_coords_dir) as f:
    lines = [line.rstrip() for line in f]

# extending text boundboxes boundaries for 1% (coordinates manipulation)
i = 0
for line in lines:
    if line:
        numbs = line.split(',')
        crop_image = image[int(int(numbs[1])*0.99):int(int(numbs[5])*1.01), int(int(numbs[0])*0.99):int(int(numbs[2])*1.01)]
        cropname = 'crop_' + str(i) + '.png'
        path = os.path.join(expanded_text_dir, cropname)
        i += 1
        cv2.imwrite(path, crop_image)

# list to store text extended boundboxes
all_boundboxes = []
all_text_files = os.listdir(expanded_text_dir)
for text in all_text_files:
    all_boundboxes.append(os.path.join(expanded_text_dir, text))

config = r'--oem 3 --psm 6'

print('--- Start recognize text from image ---')

for boundbox in all_boundboxes:
    img_crop = cv2.imread(boundbox)
    img_rgb = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img_rgb, config=config))

print("------ Done -------")
