from Config import *
from ImageHandler import *
from DataStructureConnector import *
from BST_examples import DataStructureExample

im_handler = ImageHandler('./test_images/20221212200354.png')
im_handler.run_pipeline()
ds_connector = DataStructureConnector(im_handler.app_config)


# print(TextElements)
# print(FigureElements)

arguments, BST_TREE, YES_TREES, NO_TREES = ds_connector.run_pipeline()

print('arguments:\n', arguments)
print('BST_TREE:\n', BST_TREE)
print('YES_TREES:\n', YES_TREES)
print('NO_TREES:\n', NO_TREES)

#DataStructureExample(arguments, BST_TREE, YES_TREES, NO_TREES)

# print(OutputData)

cv2.waitKey()
cv2.destroyAllWindows()
