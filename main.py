from Config import *
from ImageHandler import *
from DataStructureConnector import *
from BST_examples import DataStructureExample

im_handler = ImageHandler('./test_images/20221228213026.png')
im_handler.run_pipeline()
ds_connector = DataStructureConnector(im_handler.app_config)

bst_tree = ds_connector.run_pipeline()

print(bst_tree.generate_code())

cv2.waitKey()
cv2.destroyAllWindows()
