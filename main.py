from set_config import *
from imageHandler import *
import re

# set an image
image = 'im004.png'  # can be filepath, PIL image or numpy array
# path to file with text boundboxes coordinates
pattern = re.search('(.+?).png', image).group(1)
text_coords_file = os.path.join('auto_text', pattern + '_text_detection.txt')

output_text = 'output_text.txt'
output_figure = 'output_figure.txt'
image_no_text = 'no_text.png'
output_text_box = 'output_text_box.txt'
output_figure_box = 'output_figure_box.txt'
output_lines_box = 'output_lines_box.txt'
edges_image = 'edges.png'

DetectText(auto_text_dir, image)
image = cv2.imread(image)
lines = ReadTextBox(text_coords_file)
all_boundboxes_text = ExpandTextBox(expanded_text_dir, output_text_box, lines, image)

RecognizeText(output_text, all_boundboxes_text)
img_inpainted = CleanImageFromText(lines, image)
img = MorphologicalEnclosing(img_inpainted, image_no_text)

DetectFigures(img, figures_dir, output_figure_box)

RecognizeFigures(figures_dir, output_figure)
CleanImageFromFigures(image_no_text, output_figure_box, edges_image)

edges = DetectLines(edges_image)
RecognizeLines(edges, output_lines_box, edges_image)

# cv2.waitKey()
# cv2.destroyAllWindows()
