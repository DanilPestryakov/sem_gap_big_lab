import cv2
# Import Craft class for text detection
from craft_text_detector import Craft
import pytesseract
import numpy as np
import os
import shutil
import re
import math
from copy import deepcopy
from PIL import Image, ImageDraw

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

def InpaintText(numbs, image):
    x0, y0, x1, y1, x2, y2, x3, y3 = [float(i) for i in numbs]

    x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
    x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
    thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)

    img_inpainted = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)

    return img_inpainted

hsv_min = np.array((0, 0, 0), np.uint8)
hsv_max = np.array((200, 200, 200), np.uint8)

config = r'--oem 3 --psm 6'

# In WINDOWS only. If you don't have tesseract executable in your PATH, include the following
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# set an image
image = 'im001.png'  # can be filepath, PIL image or numpy array
pattern = re.search('(.+?).png', image).group(1)
output_text = 'output_text.txt'
output_figure = 'output_figure.txt'

# Create all paths needed
# path to automatically detected Craft text pieces
auto_text_dir = os.path.join('auto_text')
# path to text pieces with expanded boundboxes for better recognition
expanded_text_dir = os.path.join('corrected_text')
# path to file with text boundboxes coordinates
text_coords_dir = os.path.join('auto_text', pattern + '_text_detection.txt')
# path to file with figure images after correcting boundboxes coordinates
figures_dir = os.path.join('corrected_figures')

# Cleaning folders if not empty
if os.path.exists(auto_text_dir):
    if os.listdir(auto_text_dir):
        shutil.rmtree(auto_text_dir, ignore_errors=False, onerror=None)

if os.path.exists(expanded_text_dir):
    if os.listdir(expanded_text_dir):
        shutil.rmtree(expanded_text_dir, ignore_errors=False, onerror=None)

if os.path.exists(figures_dir):
    if os.listdir(figures_dir):
        shutil.rmtree(figures_dir, ignore_errors=False, onerror=None)

# Check if folders exist, creating if they do not
if not os.path.exists(auto_text_dir):
    os.makedirs(auto_text_dir)
if not os.path.exists(expanded_text_dir):
    os.makedirs(expanded_text_dir)
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

print('Start detect text from image')

# create a craft instance
craft = Craft(output_dir=auto_text_dir, crop_type="poly", cuda=False)
# apply craft text detection and export detected regions to output directory
prediction_result = craft.detect_text(image)
# unload models from ram/gpu
craft.unload_craftnet_model()
craft.unload_refinenet_model()

print('Done')

# reading the image
image = cv2.imread(image)

# reading text coordinates, removing the new line characters
with open(text_coords_dir) as f:
    lines = [line.rstrip() for line in f]

# extending text boundboxes boundaries for 1% (coordinates manipulation)
f = open("output_text_box.txt", "w+") # file to write final coordinates of the text
i = 0
text_coords = np.empty((1, 8))
str1 = " "
for line in lines:
    if line:
        numbs = line.split(',')
        y_up = int(int(numbs[1])*0.99)
        y_down = int(int(numbs[5])*1.01)
        x_left = int(int(numbs[0])*0.99)
        x_right = int(int(numbs[2])*1.01)
        text_coords = x_left, y_up, x_right, y_up, x_left, y_down, x_right, y_down
        text_coords = [str(i) for i in text_coords]
        crop_image = image[y_up:y_down, x_left:x_right]
        cropname = 'crop_' + str(i) + '.png'
        path = os.path.join(expanded_text_dir, cropname)
        i += 1
        cv2.imwrite(path, crop_image)
        f.write(str1.join(text_coords))
        f.write('\n')
f.close()

# list to store text extended boundboxes
all_boundboxes_text = []
all_text_files = os.listdir(expanded_text_dir)
for text in all_text_files:
    all_boundboxes_text.append(os.path.join(expanded_text_dir, text))

print('Start recognize text from image')

with open(output_text, 'w+') as f:  # file to write scheme text
    for boundbox in all_boundboxes_text:
        img_crop = cv2.imread(boundbox)
        img_rgb = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
        f.write(pytesseract.image_to_string(img_rgb, config=config))

print("Done")

# cleaning image from text
# x0, y0, x1, y1, x2, y2, x3, y3
img_inpainted = deepcopy(image)
for line in lines:
    if line:
        numbs = line.split(',')
        img_inpainted = InpaintText(numbs, img_inpainted)

# cv2.imshow('Inpainted image', img_inpainted)

# Morthological enclosing

print('Start morthological enclosing')

img_not = cv2.bitwise_not(img_inpainted)
# cv.imshow("invert", img_not)

kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(img_not, kernel, iterations=2)
# cv.imshow('dilation', dilation)

erosion = cv2.erode(dilation, kernel, iterations=2)
# cv.imshow('erosion', erosion)

img = cv2.bitwise_not(erosion)
# cv2.imshow("invert 2", img)
print("Done")

# Detect figures

print('Start detect figures from image')
partimg = deepcopy(img)

height, width, _ = img.shape
image_size = height * width
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # change color model BGR to HSV
thresh = cv2.inRange(hsv, hsv_min, hsv_max)  # apply color filter

contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

figure_coords = np.empty((1, 8))

f = open("output_figure_box.txt", "w+") # file to write final coordinates of figures
str2 = " "
j = 0

# iterate all contours found cycle
# extend figure boundbox to 3%
for cnt in contours0:
    rect = cv2.minAreaRect(cnt)  # try to emplace rectangle
    box = cv2.boxPoints(rect)  # find 4 rectangle coordinates
    box = np.int0(box)  # coordinates round
    area = int(rect[1][0] * rect[1][1])  # calculate area
    # if area > 0.001*image_size and area < 0.1*image_size:
    if area > 5000 and area < 20000:
        # cv2.drawContours(img, [box], -1, (255, 0, 0), 5)  # draw rectangle
        x0, x1, x2, x3 = box[:, 0]
        y0, y1, y2, y3 = box[:, 1]
        y_up = int(y1*0.97)
        y_down = int(y3*1.03)
        x_left = int(x0*0.97)
        x_right = int(x2*1.03)
        figure_coords = x_left, y_up, x_right, y_up, x_left, y_down, x_right, y_down
        figure_coords = [str(i) for i in figure_coords]
        crop_image = img[y_up:y_down, x_left:x_right]
        cropname = 'crop_' + str(j) + '.png'
        path = os.path.join(figures_dir, cropname)
        j += 1
        cv2.imwrite(path, crop_image)

        f.write(str2.join(figure_coords))
        f.write('\n')

f.close()

print("Done")

print('Start recognize figures from image')

# list to store text extended boundboxes
all_boundboxes_figures = []
all_figure_files = os.listdir(figures_dir)
for figure in all_figure_files:
    all_boundboxes_figures.append(os.path.join(figures_dir, figure))

with open(output_figure, 'w+') as f: # file to write scheme figures
    for boundbox in all_boundboxes_figures:

        # reading image
        img1 = cv2.imread(boundbox)
        # making border around image using copyMakeBorder
        img = cv2.copyMakeBorder(img1, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        # converting image into grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # print(len(contours))
        i = 0
        # list for storing names of shapes
        for contour in contours:
            # here we are ignoring first counter because
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)

            # cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)

            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / (M['m00'] + 1e-8))
                y = int(M['m01'] / (M['m00']) + 1e-8)

            if len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                figure_name = 'Quadrilateral'

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                figure_name = 'Pentagon'

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                figure_name = 'Hexagon'

            else:
                cv2.putText(img, 'Circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                figure_name = 'Circle'

        f.write(figure_name)
        f.write('\n')

print("Done")

# TODO inpaint figures
# Delete figures
image = Image.open('im001.png')
draw = ImageDraw.Draw(image)
draw.polygon(((x0, y0), (x1, y1), (x2, y2), (x3, y3)), fill="white")
image.save('result.png')

# cv2.imshow('Inpainted image 2', img_inpainted)  # draw result image

# cv2.imshow('contours', img)  # draw result image

# Recognize figures
print('Start recognize figures from image')
