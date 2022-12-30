import pytesseract
import os
import shutil
import re


class Config:
    # set global config variables

    HELP_DIR = 'detection_help_dir'

    OUTPUT_TEXT = f'./{HELP_DIR}/output_text.txt'
    OUTPUT_FIGURE = f'./{HELP_DIR}/output_figure.txt'
    OUTPUT_TEXT_BOX = f'./{HELP_DIR}/output_text_box.txt'
    OUTPUT_FIGURE_BOX = f'./{HELP_DIR}/output_figure_box.txt'
    OUTPUT_LINES_BOX = f'./{HELP_DIR}/output_lines_box.txt'
    OUTPUT_LINES_POINT = f'./{HELP_DIR}/output_lines_point.txt'
    OUTPUT_FIGURES_POINT = f'./{HELP_DIR}/output_figures_point.txt'
    OUTPUT_TEXT_POINT = f'./{HELP_DIR}/output_text_point.txt'
    IMAGE_NO_TEXT = f'./{HELP_DIR}/no_text.png'
    EDGES_IMAGE = f'./{HELP_DIR}/edges.png'

    # path to automatically detected Craft text pieces
    AUTO_TEXT_DIR = os.path.join('auto_text')

    # path to text pieces with expanded boundboxes for better recognition
    EXPANDED_TEXT_DIR = os.path.join('corrected_text')

    # path to file with figure images after correcting boundboxes coordinates
    FIGURES_DIR = os.path.join('corrected_figures')

    # Pytesseract configuration for better text recognition
    # oem - Engine Mode
    # psm - Page Segmentation Mode
    TESSERACT_CONFIG = r'--oem 3 --psm 6'

    def __init__(self, image):
        # init directories

        # In WINDOWS only. If you don't have tesseract executable in your PATH, include the following
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

        # Create all paths needed

        # Cleaning folders if not empty
        if os.path.exists(Config.AUTO_TEXT_DIR):
            if os.listdir(Config.AUTO_TEXT_DIR):
                shutil.rmtree(Config.AUTO_TEXT_DIR, ignore_errors=False, onerror=None)

        if os.path.exists(Config.EXPANDED_TEXT_DIR):
            if os.listdir(Config.EXPANDED_TEXT_DIR):
                shutil.rmtree(Config.EXPANDED_TEXT_DIR, ignore_errors=False, onerror=None)

        if os.path.exists(Config.FIGURES_DIR):
            if os.listdir(Config.FIGURES_DIR):
                shutil.rmtree(Config.FIGURES_DIR, ignore_errors=False, onerror=None)

        if os.path.exists(Config.HELP_DIR):
            if os.listdir(Config.HELP_DIR):
                shutil.rmtree(Config.HELP_DIR, ignore_errors=False, onerror=None)

        # Check if folders exist, creating if they do not
        if not os.path.exists(Config.AUTO_TEXT_DIR):
            os.makedirs(Config.AUTO_TEXT_DIR)
        if not os.path.exists(Config.EXPANDED_TEXT_DIR):
            os.makedirs(Config.EXPANDED_TEXT_DIR)
        if not os.path.exists(Config.FIGURES_DIR):
            os.makedirs(Config.FIGURES_DIR)
        if not os.path.exists(Config.HELP_DIR):
            os.makedirs(Config.HELP_DIR)

        # path to file with text boundboxes coordinates
        pattern = re.search('(.+?).png', image).group(1).split('/')[-1]
        self.TEXT_COORDS_FILE = os.path.join('auto_text', pattern + '_text_detection.txt')
