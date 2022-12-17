from Config import *
from ImageHandler import *
from DataStructureConnector import *
from BST_examples import DataStructureExample

im_handler = ImageHandler('./test_images/20221217210344.png')
im_handler.run_pipeline()
ds_connector = DataStructureConnector(im_handler.app_config)

SCHEME = ds_connector.run_pipeline()

DataStructureExample(SCHEME)

cv2.waitKey()
cv2.destroyAllWindows()
