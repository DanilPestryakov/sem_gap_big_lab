import math


class DataStructureConnector:
    def __init__(self, config):
        self.app_config = config
        self.text_elements = None
        self.figure_elements = None

    def run_pipeline(self):
        self.text_elements = DataStructureConnector.connect_elements_and_boxes(
            self.app_config.OUTPUT_TEXT, self.app_config.OUTPUT_TEXT_BOX, self.app_config.OUTPUT_TEXT_POINT)
        self.figure_elements = DataStructureConnector.connect_elements_and_boxes(
            self.app_config.OUTPUT_FIGURE, self.app_config.OUTPUT_FIGURE_BOX, self.app_config.OUTPUT_FIGURES_POINT)
        return self.init_data_structure()

    @classmethod
    def connect_elements_and_boxes(cls, text_file, box_file, coord_file):
        scheme_elements = []
        ft = open(text_file)
        fb = open(box_file)
        fc = open(coord_file)
        text = ft.readlines()
        box = fb.readlines()
        coord = fc.readlines()

        for i in range(len(text)):
            scheme_elements.append(
                {"text": text[i].strip(), "box": box[i].strip(), "coord": coord[i].strip(), "code": ''})

        for elem in scheme_elements:
            elem["box"] = list(map(lambda x: int(x), elem["box"].split()))
            elem["coord"] = list(map(lambda x: int(x), elem["coord"].split()))

        return scheme_elements

    def apply_text_to_figures(self, lst):
        for elem in lst:
            x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
            for code in self.text_elements:
                x, y = code['coord']
                if (x0 < x < x1) and (y1 < y < y3):
                    elem['code'] = code['text']

    def apply_text_to_figures_arguments(self, lst):
        for elem in lst:
            x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
            elem['code'] = []
            for code in self.text_elements:
                x, y = code['coord']
                if (x0 < x < x1) and (y0 < y < y2):
                    elem['code'].append(code['text'])

    def init_data_structure(self):

        EPS_DIST = 10

        newlist = sorted(self.figure_elements, key=lambda i: i['coord'][1], reverse=False)
        # print('newlist', newlist)

        temp_list = []  # filtered from circles (program begin/end)
        circle = [d if d['text'] == 'Circle' else temp_list.append(d) for d in newlist]
        circle = list(filter(lambda item: item is not None, circle))
        newlist.clear()

        newlist_circle = sorted(circle, key=lambda i: i['coord'][1], reverse=False)
        program_begin = newlist_circle[0]
        program_end = newlist_circle[1]
        newlist_circle[1]['text'] = 'CircleEndPoint'

        total_list = []  # filtered from program arguments figure
        arguments = [d if d['text'] == 'Quadrilateral' and
                          abs(d['coord'][1] - program_begin['coord'][1]) < EPS_DIST else total_list.append(d) for d
                     in
                     temp_list]
        arguments = list(filter(lambda item: item is not None, arguments))
        temp_list.clear()

        points = []
        with open(self.app_config.OUTPUT_LINES_POINT) as f:
            lines = f.readlines()
            for line in lines:
                elem = {'text': 'EndPoint'}
                x, y = list(map(lambda x: int(x), line.split()))
                elem['box'] = [x, y, x, y, x, y, x, y]
                elem['coord'] = [x, y]
                elem['code'] = ''
                points.append(elem)

        self.apply_text_to_figures(total_list)
        self.apply_text_to_figures(newlist_circle)
        self.apply_text_to_figures_arguments(arguments)

        total_list.extend(newlist_circle)
        total_list.extend(arguments)
        total_list.extend(points)

        return total_list
"""
    def init_data_structure(self):
        EPS_DIST = 10

        newlist = sorted(self.figure_elements, key=lambda i: i['coord'][1], reverse=False)

        list1 = []  # filtered from circles (program begin/end)
        circle = [d if d['text'] == 'Circle' else list1.append(d) for d in newlist]
        circle = list(filter(lambda item: item is not None, circle))

        newlist_circle = sorted(circle, key=lambda i: i['coord'][1], reverse=False)
        program_begin = newlist_circle[0]
        program_end = newlist_circle[1]

        list2 = []  # filtered from program arguments figure
        arguments = [d if d['text'] == 'Quadrilateral' and
                          abs(d['coord'][1] - program_begin['coord'][1]) < EPS_DIST else list2.append(d) for d
                     in
                     list1]
        arguments = list(filter(lambda item: item is not None, arguments))
        #print(newlist)
        #print(arguments)

        points = []
        with open(self.app_config.OUTPUT_LINES_POINT) as f:
            lines = f.readlines()
            for line in lines:
                x, y = list(map(lambda x: int(x), line.split()))
                points.append([x, y])

        hexagon = [d for d in list2 if d['text'] == 'HexagonCondition' or d['text'] == 'HexagonCycle']
        hexagon_end_point = [d['coord'] for d in list2 if d['text'] == 'HexagonCycleEndPoint']
        points.extend(hexagon_end_point)

        #    common_length_dist = len(list2)
        #    for i in range(common_length_dist):
        #        distance = []
        #        for j in range(len(Points)):
        #            for k in range(len(hexagon)):

        cond_levels = [d['coord'][0] for d in hexagon]
        cond_levels.append(1000)

        yes_trees_elems = []
        no_trees_elems = []
        bst_tree_elems = []
        BST_TREE = []
        YES_TREES = []
        NO_TREES = []

        if points:
            for i in range(len(hexagon)):
                yes_trees_elems.append(hexagon[i])
                no_trees_elems.append(hexagon[i])
                for elem in list2:
                    if hexagon[i]['coord'][1] < elem['coord'][1] < points[i][1] and int(cond_levels[i] * 0.9) < \
                            elem['coord'][0] < int(cond_levels[i] * 1.1):
                        yes_trees_elems.append(elem)
                    elif hexagon[i]['coord'][1] < elem['coord'][1] < points[i][1] and int(cond_levels[i] * 1.1) < \
                            elem['coord'][0] < int(cond_levels[i] * 4.0):
                        no_trees_elems.append(elem)
                    else:
                        bst_tree_elems.append(elem)
                yes_trees = sorted(yes_trees_elems, key=lambda i: i['coord'][1], reverse=False)
                no_trees = sorted(no_trees_elems, key=lambda i: i['coord'][1], reverse=False)
                YES_TREES.append(yes_trees)
                NO_TREES.append(no_trees)

        bst_tree_elems.append(program_begin)
        bst_tree_elems.append(program_end)
        bst_tree = sorted(bst_tree_elems, key=lambda i: i['coord'][1], reverse=False)
        BST_TREE.append(bst_tree)

        self.apply_text_to_figures(BST_TREE)
        self.apply_text_to_figures(YES_TREES)
        self.apply_text_to_figures(NO_TREES)
        self.apply_text_to_figures_arguments(arguments)

        return arguments, BST_TREE, YES_TREES, NO_TREES
"""