from Config import *
from ImageHandler import *
from DataStructure import *
from BST_examples import DataStructureExample

im_handler = ImageHandler('./test_images/test1.png')
im_handler.run_pipeline()

TextElements = ConnectElementsAndBoxes(Config.OUTPUT_TEXT, Config.OUTPUT_TEXT_BOX, Config.OUTPUT_TEXT_POINT)
FigureElements = ConnectElementsAndBoxes(Config.OUTPUT_FIGURE, Config.OUTPUT_FIGURE_BOX, Config.OUTPUT_FIGURES_POINT)

# print(TextElements)
# print(FigureElements)

arguments, BST_TREE, YES_TREES, NO_TREES = DataStructure(FigureElements, TextElements, Config.OUTPUT_LINES_POINT)

print('arguments:\n', arguments)
print('BST_TREE:\n', BST_TREE)
print('YES_TREES:\n', YES_TREES)
print('NO_TREES:\n', NO_TREES)

DataStructureExample(arguments, BST_TREE, YES_TREES, NO_TREES)

# print(OutputData)

cv2.waitKey()
cv2.destroyAllWindows()
