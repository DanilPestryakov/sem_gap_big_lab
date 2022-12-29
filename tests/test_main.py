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
            while original_str_item[j] == '\t':
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

    print(f'\n\nGenerated code:\n\n{predicted_code}\n\n')
    print(f'Original code:\n\n{original_code}\n\n')
    print(f'Metric: {get_metric(predicted_code, original_code)}')


if __name__ == "__main__":
    tests = [test_20221214231758]
    for test in tests:
        test()
