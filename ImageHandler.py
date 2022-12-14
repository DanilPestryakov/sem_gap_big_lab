import cv2
from craft_text_detector import Craft  # Import Craft class for text detection
import numpy as np
import scipy.cluster.hierarchy as hcluster
import math
from copy import deepcopy
from PIL import Image, ImageDraw
import os
from Config import pytesseract
from Config import Config


class ImageHandler:
    def __init__(self, image):
        self.image = image
        self.app_config = Config(image)
        self.image_arr = []
        self.lines = None
        self.all_boundboxes_text = []
        self.img_inpainted = None
        self.enclosed_img = []
        self.edges = None

    def run_pipeline(self):
        self.detect_text()
        self.image_arr = cv2.imread(self.image)
        self.read_text_box()
        self.expand_text_box()
        self.recognize_text()
        self.clean_image_from_text()
        self.morphological_enclosing()
        self.detect_figures()
        self.recognize_figures()
        self.clean_image_from_figures()
        self.detect_lines()
        self.recognize_lines()
        self.lines_points()
        ImageHandler.box_points(self.app_config.OUTPUT_FIGURE_BOX, self.app_config.OUTPUT_FIGURES_POINT)
        ImageHandler.box_points(self.app_config.OUTPUT_TEXT_BOX, self.app_config.OUTPUT_TEXT_POINT)


    @classmethod
    def midpoint(cls, x1, y1, x2, y2):
        x_mid = int((x1 + x2) / 2)
        y_mid = int((y1 + y2) / 2)
        return x_mid, y_mid

    @classmethod
    def masscenter(cls, x0, y0, x1, y2):
        center_x = int((x0 + x1) / 2)
        center_y = int((y0 + y2) / 2)
        return center_x, center_y

    @classmethod
    def inpaint_text(cls, numbs, image):
        #TODO clear from other
        x0, y0, x1, y1, x2, y2, x3, y3, *other = [float(i) for i in numbs]
        x_mid0, y_mid0 = ImageHandler.midpoint(x1, y1, x2, y2)
        x_mid1, y_mid1 = ImageHandler.midpoint(x0, y0, x3, y3)
        thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
        img_inpainted = cv2.inpaint(image, mask, 6, cv2.INPAINT_NS)
        return img_inpainted

    @classmethod
    def identify_hexagon(cls, vertexes):
        EPS_HEX = 4
        lengths = []
        # vertexes.shape (6, 1, 2)
        vertexes_coords = sorted(vertexes, key=lambda v: v[:][0][1], reverse=False)
        max_edge = max(vertexes_coords[-1][0][0], vertexes_coords[-2][0][0]) - \
            min(vertexes_coords[-1][0][0], vertexes_coords[-2][0][0])

        for i in range(len(vertexes) - 1):
            x0, y0, x1, y1 = vertexes[i][0][0], vertexes[i][0][1], vertexes[i + 1][0][0], vertexes[i + 1][0][1]
            lengths.append(math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))
        x0, y0, x1, y1 = vertexes[0][0][0], vertexes[0][0][1], vertexes[len(vertexes) - 1][0][0], \
                         vertexes[len(vertexes) - 1][0][1]
        lengths.append(math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))
        lengths.sort()

        if abs(lengths[-1] - lengths[-2]) < EPS_HEX:
            return "HexagonCondition"
        elif abs(max_edge - lengths[-1]) > 1:
            return "HexagonCycleEndPoint"
        else:
            return "HexagonCycle"

    def detect_text(self):
        # create a craft instance
        craft = Craft(output_dir=self.app_config.AUTO_TEXT_DIR, crop_type="poly", cuda=False)
        # apply craft text detection and export detected regions to output directory
        # prediction_result
        craft.detect_text(self.image)
        # unload models from ram/gpu
        craft.unload_craftnet_model()
        craft.unload_refinenet_model()
        print("Text detected")

    def read_text_box(self):
        # reading text coordinates, removing the new line characters
        with open(self.app_config.TEXT_COORDS_FILE) as f:
            lines = [line.rstrip() for line in f]
        self.lines = lines

    def expand_text_box(self):
        # extending text boundboxes boundaries for 2% (coordinates manipulation)
        EPS = 0.02
        f = open(self.app_config.OUTPUT_TEXT_BOX, "w+")  # file to write final coordinates of the text
        i = 0
        str1 = " "
        for line in self.lines:
            if line:
                numbs = line.split(',')
                y_up = int(int(numbs[1]) * (1. - EPS))
                y_down = int(int(numbs[5]) * (1. + EPS))
                x_left = int(int(numbs[0]) * (1. - EPS))
                x_right = int(int(numbs[2]) * (1. + EPS))
                text_coords = x_left, y_up, x_right, y_up, x_left, y_down, x_right, y_down
                text_coords = [str(i) for i in text_coords]
                crop_image = self.image_arr[y_up:y_down, x_left:x_right]
                cropname = 'crop_' + str(i) + '.png'
                path = os.path.join(self.app_config.EXPANDED_TEXT_DIR, cropname)
                i += 1
                cv2.imwrite(path, crop_image)
                f.write(str1.join(text_coords))
                f.write('\n')
        f.close()

        # list to store text extended boundboxes
        all_text_files = os.listdir(self.app_config.EXPANDED_TEXT_DIR)
        for text in all_text_files:
            self.all_boundboxes_text.append(os.path.join(self.app_config.EXPANDED_TEXT_DIR, text))

        return self.all_boundboxes_text

    def recognize_text(self):
        with open(self.app_config.OUTPUT_TEXT, 'w+') as f:  # file to write scheme text
            for boundbox in self.all_boundboxes_text:
                img_crop = cv2.imread(boundbox)
                img_rgb = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
                f.write(pytesseract.image_to_string(img_rgb, config=self.app_config.TESSERACT_CONFIG))
        print("Text recognized")

    def clean_image_from_text(self):
        # cleaning image from text
        # x0, y0, x1, y1, x2, y2, x3, y3
        #TODO check numbs
        self.img_inpainted = deepcopy(self.image_arr)
        for line in self.lines:
            if line:
                numbs = line.strip().split(',')
                print(numbs)
                self.img_inpainted = ImageHandler.inpaint_text(numbs, self.img_inpainted)

    def morphological_enclosing(self):
        img_not = cv2.bitwise_not(self.img_inpainted)
        # cv.imshow("invert", img_not)

        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(img_not, kernel, iterations=1)
        # cv.imshow('dilation', dilation)

        erosion = cv2.erode(dilation, kernel, iterations=1)
        # cv.imshow('erosion', erosion)

        self.enclosed_img = cv2.bitwise_not(erosion)
        cv2.imwrite(self.app_config.IMAGE_NO_TEXT, self.enclosed_img)

    def detect_figures(self):

        MIN_AREA = 1000
        MAX_AREA = 20000
        EPS = 0.02  # figure boundbox 2% extension

        height, width, _ = self.enclosed_img.shape
        # image_size = height * width
        hsv = cv2.cvtColor(self.enclosed_img, cv2.COLOR_BGR2HSV)  # change color model BGR to HSV
        hsv_min = np.array((0, 0, 0), np.uint8)
        hsv_max = np.array((200, 200, 200), np.uint8)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)  # apply color filter

        contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # figure_coords = np.empty((1, 8))
        f = open(self.app_config.OUTPUT_FIGURE_BOX, "w+")  # file to write final coordinates of figures
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
            if area > MIN_AREA and area < MAX_AREA:
                # cv2.drawContours(img, [box], -1, (255, 0, 0), 5)  # draw rectangle
                x0, x1, x2, x3 = box[:, 0]
                y0, y1, y2, y3 = box[:, 1]
                y_up = int(y1 * (1. - EPS))
                y_down = int(y3 * (1. + EPS))
                x_left = int(x0 * (1. - 6*EPS))
                x_right = int(x2 * (1. + 2*EPS))
                figure_coords = x_left, y_up, x_right, y_up, x_left, y_down, x_right, y_down
                figure_coords = [str(i) for i in figure_coords]
                crop_image = self.enclosed_img[y_up:y_down, x_left:x_right]
                cropname = 'crop_' + str(j) + '.png'
                path = os.path.join(self.app_config.FIGURES_DIR, cropname)
                j += 1
                cv2.imwrite(path, crop_image)
                f.write(str2.join(figure_coords))
                f.write('\n')

        f.close()
        print("Figures detected")

    def clean_image_from_figures(self):
        image = Image.open(self.app_config.IMAGE_NO_TEXT)
        draw = ImageDraw.Draw(image)
        f = open(self.app_config.OUTPUT_FIGURE_BOX)
        lines = f.readlines()
        for line in lines:
            x_left, y_up, x_right, y_up, x_left, y_down, x_right, y_down = list(map(lambda x: int(x), line.split()))
            draw.polygon(((x_left, y_up), (x_right, y_up), (x_right, y_down), (x_left, y_down)), fill="white")
            image.save(self.app_config.EDGES_IMAGE)  # inpaint figures and save result (only edges)

    def recognize_figures(self):
        # list to store text extended boundboxes
        all_boundboxes_figures = []
        all_figure_files = os.listdir(self.app_config.FIGURES_DIR)
        for figure in all_figure_files:
            all_boundboxes_figures.append(os.path.join(self.app_config.FIGURES_DIR, figure))

        with open(self.app_config.OUTPUT_FIGURE, 'w+') as f:  # file to write scheme figures
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
                for contour in contours[1:]:
                    # here we are ignoring first counter because
                    # findcontour function detects whole image as shape
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

                        figure_name = ImageHandler.identify_hexagon(approx)
                        # figure_name = 'Hexagon'

                        # print('approx = ', approx)
                        # cv2.imwrite('hexa.png', img)

                    else:
                        cv2.putText(img, 'Circle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                        figure_name = 'Circle'

                f.write(figure_name)
                f.write('\n')
        print("Figures recognized")

    def detect_lines(self):
        # Read image
        image = cv2.imread(self.app_config.EDGES_IMAGE)
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Use canny edge detection
        self.edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        print("Lines detected")

    def recognize_lines(self):
        # Read image
        image = cv2.imread(self.app_config.EDGES_IMAGE)
        # Apply HoughLinesP method to
        # to directly obtain line end points
        lines_list = []
        lines = cv2.HoughLinesP(
            self.edges,  # Input edge image
            1,  # Distance resolution in pixels
            np.pi / 180,  # Angle resolution in radians
            threshold=20,  # Min number of votes for valid line
            minLineLength=15,  # Min allowed length of line
            maxLineGap=10  # Max allowed gap between line for joining them
        )
        # Iterate over points
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]
            # Draw the lines joining the points
            # On the original image
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Maintain a simples lookup list for points
            lines_list.append([x1, y1, x2, y2])

        # Show the result image
        cv2.imshow('edges', image)

        str3 = " "
        with open(self.app_config.OUTPUT_LINES_BOX, "w+") as f:
            for line in lines_list:
                line_coords = [str(i) for i in line]
                f.write(str3.join(line_coords))
                f.write('\n')

        print("Lines recognized")

    def lines_points(self):

        EPS = 3  # accuracy of assuming line horizontal/vertical (in pixels)
        EPS_POINT = 20  # accuracy of side line entrance to main line

        # read lines points coordinates
        f = open(self.app_config.OUTPUT_LINES_BOX)
        Horizontal = []
        Vertical = []
        lines = f.readlines()
        for line in lines:
            x0, y0, x1, y1 = list(map(lambda x: int(x), line.split()))
            if abs(x0 - x1) < EPS:
                Vertical.append(list([x0, y0, x1, y1]))
            else:
                Horizontal.append(list([x0, y0, x1, y1]))
        f.close()

        # sort lines orientation
        # x: left - right point
        # y: up - down point
        for i in range(len(Vertical)):
            x0, y0, x1, y1 = Vertical[i]
            if y0 > y1:
                Vertical[i] = list([x1, y1, x0, y0])

        for i in range(len(Horizontal)):
            x0, y0, x1, y1 = Horizontal[i]
            if x0 > x1:
                Horizontal[i] = list([x1, y1, x0, y0])

        points_lst = []

        for line_vert in Vertical:
            x0_v, y0_v, x1_v, y1_v = line_vert
            for line_horiz in Horizontal:
                x0_h, y0_h, x1_h, y1_h = line_horiz
                if (abs(x0_h - x0_v) < EPS_POINT) and (y0_v < y0_h < y1_v):
                    points_lst.append([x0_v, y0_h])

        points_list = []
        if len(points_lst) > 1:
            thresh = 5
            clusters = hcluster.fclusterdata(points_lst, thresh, criterion="distance")
            clusters_id = list(set(clusters))

            for id in clusters_id:
                nearest_points = []
                for i in range(len(clusters)):
                    if clusters[i] == id:
                        nearest_points.append(points_lst[i])
                center_x = int(sum([elem[0] for elem in nearest_points]) / len(nearest_points))
                center_y = int(sum([elem[1] for elem in nearest_points]) / len(nearest_points))
                points_list.append([center_x, center_y])
                points_lst.clear()

        with open(self.app_config.OUTPUT_LINES_POINT, 'w+') as f:
            if len(points_list) > 1:
                for elem in points_list:
                    x, y = elem
                    point_coords = str(x) + " " + str(y)
                    f.write(point_coords)
                    f.write('\n')

    @classmethod
    def box_points(cls, output_figure_box, output_figures_point):
        fr = open(output_figure_box)
        fw = open(output_figures_point, "w+")
        lines = fr.readlines()
        for line in lines:
            x0, y0, x1, y1, x2, y2, x3, y3 = list(map(lambda x: int(x), line.split()))
            xc, yc = ImageHandler.masscenter(x0, y0, x1, y2)
            point_coords = str(xc) + " " + str(yc)
            fw.write(point_coords)
            fw.write('\n')
        fr.close()
        fw.close()
