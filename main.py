from ImageHandler import *
from DataStructureConnector import *

im_handler = ImageHandler('./test_images/20221214231758.png')
im_handler.run_pipeline()
ds_connector = DataStructureConnector(im_handler.app_config)

bst_tree = ds_connector.run_pipeline()

print(bst_tree.generate_code())

cv2.waitKey()
cv2.destroyAllWindows()
