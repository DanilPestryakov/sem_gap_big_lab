from Config import *
from ImageHandler import *
from DataStructure import *
from BST_examples import DataStructureExample

im_handler = ImageHandler('./test_images/test1.png')
im_handler.run_pipeline()

DetectText(Config.AUTO_TEXT_DIR, image)
image = cv2.imread(image)
lines = ReadTextBox(text_coords_file)
all_boundboxes_text = ExpandTextBox(Config.EXPANDED_TEXT_DIR, output_text_box, lines, image)

RecognizeText(output_text, all_boundboxes_text)
img_inpainted = CleanImageFromText(lines, image)
img = MorphologicalEnclosing(img_inpainted, image_no_text)

DetectFigures(img, Config.FIGURES_DIR, output_figure_box)

RecognizeFigures(Config.FIGURES_DIR, output_figure)
CleanImageFromFigures(image_no_text, output_figure_box, edges_image)

edges = DetectLines(edges_image)
RecognizeLines(edges, output_lines_box, edges_image)

LinesPoints(output_lines_box, output_lines_point)
BoxPoints(output_figure_box, output_figures_point)
BoxPoints(output_text_box, output_text_point)

TextElements = ConnectElementsAndBoxes(output_text, output_text_box, output_text_point)
FigureElements = ConnectElementsAndBoxes(output_figure, output_figure_box, output_figures_point)

# print(TextElements)
# print(FigureElements)

arguments, BST_TREE, YES_TREES, NO_TREES = DataStructure(FigureElements, TextElements, output_lines_point)

print('arguments:\n', arguments)
print('BST_TREE:\n', BST_TREE)
print('YES_TREES:\n', YES_TREES)
print('NO_TREES:\n', NO_TREES)

DataStructureExample(arguments, BST_TREE, YES_TREES, NO_TREES)

# print(OutputData)

cv2.waitKey()
cv2.destroyAllWindows()
