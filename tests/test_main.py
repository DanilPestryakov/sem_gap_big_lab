from ImageHandler import ImageHandler
from DataStructureConnector import DataStructureConnector
from fuzzywuzzy import fuzz


def get_metric(predicted_str: str, original_str: str) -> float:
    predicted_str_list = predicted_str.split('\n')
    original_str_list = original_str.split('\n')
    result_metric = 0.0
    if len(predicted_str_list) != len(original_str_list):
        return (abs(len(predicted_str_list) - len(original_str_list)) / len(original_str_list)) * 0.2
    else:
        result_metric = 0.2
        str_num_with_success_tab = len(original_str_list)
        for num, original_str_item in enumerate(original_str_list):
            i = 0
            j = 0
            while original_str_item[i] == '\t':
                i += 1
            while predicted_str_list[num][j] == '\t':
                j += 1
            if i != j:
                str_num_with_success_tab -= 1
        if str_num_with_success_tab != len(original_str_list):
            return result_metric + 0.4 * str_num_with_success_tab / len(original_str_list)
        else:
            result_metric += 0.4
            percent_of_success_strings = 0
            for num, original_str_item in enumerate(original_str_list):
                percent_of_success_strings += fuzz.ratio(original_str_item, predicted_str_list[num])
            result_metric += (percent_of_success_strings * 0.4 / (100 * len(original_str_list)))
    return result_metric


def test_20221214231758():
    im_handler = ImageHandler('../test_images/20221214231758.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def decrement():\n' \
                    '\twhile a>b:\n' \
                    '\t\ta=a-1\n' \
                    '\tprint(a)'
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221214231758.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221216222919():
    im_handler = ImageHandler('../test_images/20221216222919.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def minimum(a=7, b=3):\n' \
                    '\tif a<b:\n' \
                    '\t\tprint(a)\n' \
                    '\telse:\n' \
                    '\t\tprint(b)'
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221216222919.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221216223250():
    im_handler = ImageHandler('../test_images/20221216223250.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def cycle():\n' \
                    '\tfor i in range(1, 11):\n' \
                    '\t\tprint(i)'
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221216223250.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221217125146():
    im_handler = ImageHandler('../test_images/20221217125146.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def maximum(a, b):\n' \
                    '\tc=a\n' \
                    '\tif b>a:\n' \
                    '\t\tc=b\n' \
                    '\tprint(c)'
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221217125146.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221217125240():
    im_handler = ImageHandler('../test_images/20221217125240.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def hello(a, b):\n' \
                    '\tprint(a, b)'
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221217125240.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221217210344():
    im_handler = ImageHandler('../test_images/20221217210344.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def is_even(n=2):\n' \
                    '\tif n==0:\n' \
                    "\t\tprint('NA')\n" \
                    "\telse:\n" \
                    "\t\tif n%2==0:\n" \
                    "\t\t\tprint('YES')\n" \
                    "\t\telse:\n" \
                    "\t\t\tprint('NO')"
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221217210344.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221220211317():
    im_handler = ImageHandler('../test_images/20221220211317.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def Max3(a, b, c):\n' \
                    '\tif a>b:\n' \
                    "\t\ttemp=a\n" \
                    "\telse:\n" \
                    "\t\ttemp=b\n" \
                    "\tif c>temp:\n" \
                    "\t\tres=c\n" \
                    "\telse:\n" \
                    "\t\tres=temp\n" \
                    "\tprint(res)"
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221220211317.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221226122142():
    im_handler = ImageHandler('../test_images/20221226122142.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def nested(a, b):\n' \
                    '\tc=a\n' \
                    '\tif b>a:\n' \
                    "\t\tc=b\n" \
                    "\telse:\n" \
                    "\t\tif b>1000:\n" \
                    '\t\t\tprint("Big!")\n' \
                    "\tprint(c)"
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221226122142.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


def test_20221226122501():
    im_handler = ImageHandler('../test_images/20221226122501.png')
    im_handler.run_pipeline()
    ds_connector = DataStructureConnector(im_handler.app_config)

    bst_tree = ds_connector.run_pipeline()
    original_code = 'def nested2(a, b):\n' \
                    '\tc=a\n' \
                    '\tif b>a:\n' \
                    "\t\tc=b\n" \
                    "\t\tif c>1000:\n" \
                    '\t\t\tprint("Big!")\n' \
                    "\tprint(c)"
    predicted_code = bst_tree.generate_code()
    if predicted_code[0] == '\n':
        predicted_code = predicted_code[1:]

    print('\n\nRun test 20221226122501.png:\n')
    print(f'Generated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


if __name__ == "__main__":
    tests = [test_20221226122501]
    for test in tests:
        test()
