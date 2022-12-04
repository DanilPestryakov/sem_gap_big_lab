import pytesseract
import os
import shutil

# In WINDOWS only. If you don't have tesseract executable in your PATH, include the following
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Pytesseract configuration for better text recognition
# oem - Engine Mode
# psm - Page Segmentation Mode
config = r'--oem 3 --psm 6'

# Create all paths needed
# path to automatically detected Craft text pieces
auto_text_dir = os.path.join('auto_text')
# path to text pieces with expanded boundboxes for better recognition
expanded_text_dir = os.path.join('corrected_text')
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
