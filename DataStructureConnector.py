import math
from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import ConditionStep, CycleStep, FuncStep, SimpleCodeStep


class DataStructureConnector:
    def __init__(self, config):
        self.app_config = config
        self.text_elements = None
        self.figure_elements = None
        self.total_list = []
        self.bst = BlockSchemeTree()

    def run_pipeline(self):
        self.text_elements = DataStructureConnector.connect_elements_and_boxes(
            self.app_config.OUTPUT_TEXT, self.app_config.OUTPUT_TEXT_BOX, self.app_config.OUTPUT_TEXT_POINT)
        self.figure_elements = DataStructureConnector.connect_elements_and_boxes(
            self.app_config.OUTPUT_FIGURE, self.app_config.OUTPUT_FIGURE_BOX, self.app_config.OUTPUT_FIGURES_POINT)
        self.init_data_structure()
        self.link_ds_with_tree()
        return self.bst

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
        self.total_list = sorted(total_list, key=lambda f: (f['coord'][1], f['coord'][0]), reverse=False)

    def has_neighbour_yes(self, elem):
        for num, item in enumerate(self.total_list):
            dist_x = abs(elem['coord'][0] - item['coord'][0])
            dist_y = item['coord'][1] - elem['coord'][1]
            if dist_x < 10 and 10 < dist_y:
                return item, num
        return {}, 0

    def get_next_step(self, elem):
        return self.has_neighbour_yes(elem)

    def has_neighbour_no(self, elem):
        for num, item in enumerate(self.total_list):
            dist_x = item['coord'][0] - elem['coord'][0]
            dist_y = item['coord'][1] - elem['coord'][1]
            if 200 < dist_x < 400 and 0 < dist_y < 100:
                return item, num
        return {}, 0

    def check_func_entry_args(self, func_idx):
        if len(self.total_list) > (func_idx + 1) \
                and self.total_list[func_idx + 1]['text'] == 'Quadrilateral' \
                and abs(self.total_list[func_idx + 1]['coord'][1] - self.total_list[func_idx]['coord'][1]) < 20 \
                and self.total_list[func_idx + 1]['coord'][0] > self.total_list[func_idx]['coord'][0]:
            return True
        return False

    def link_ds_with_tree(self):
        cur_tree = self.bst
        cur_step = cur_tree
        stack = []
        i = 0
        start_yes = False
        while True:
            cur_fig = self.total_list[i]['text']
            if cur_fig == 'CircleEndPoint':
                break
            elif cur_fig == 'Circle':
                start_yes = False
                if self.check_func_entry_args(i):
                    cur_step = FuncStep(self.total_list[i]['code'], self.total_list[i + 1]['code'], cur_step, cur_tree)
                    i += 2
                else:
                    cur_step = FuncStep(self.total_list[i]['code'], [], cur_step, cur_tree)
                    i += 1
            elif cur_fig == 'Quadrilateral':
                cur_step = SimpleCodeStep(self.total_list[i]['code'], cur_step, cur_tree)
                if start_yes:
                    step, new_i = self.get_next_step(self.total_list[i])
                    if new_i == 0:
                        i += 1
                    else:
                        i = new_i
                else:
                    i += 1
                start_yes = False
            elif cur_fig == 'HexagonCondition':
                start_yes = False
                no_tree, idx_of_no_subtree = self.has_neighbour_no(self.total_list[i])
                yes_tree, idx_of_yes_subtree = self.has_neighbour_yes(self.total_list[i])
                stack.append(
                    (self.total_list[i], cur_step, cur_tree, yes_tree, no_tree, i, idx_of_yes_subtree,
                     idx_of_no_subtree, None))
                if no_tree:
                    i = idx_of_no_subtree
                else:
                    i = idx_of_yes_subtree
                cur_tree = BlockSchemeTree()
                cur_step = cur_tree
            elif cur_fig == 'EndPoint':
                cur_cond = stack.pop()
                if cur_cond[4]:
                    stack.append((cur_cond[0], cur_cond[1], cur_cond[2], cur_cond[3], False, cur_cond[5], cur_cond[6],
                                  cur_cond[7], cur_tree))
                    i = cur_cond[6]
                    start_yes = True
                    cur_tree = BlockSchemeTree()
                    cur_step = cur_tree
                else:
                    cur_step = ConditionStep(cur_cond[0]['code'], cur_tree, cur_cond[8], cur_cond[1], cur_cond[2])
                    cur_tree = cur_cond[2]
                    i += 1
            elif cur_fig == 'HexagonCycle':
                start_yes = False
                iter_tree, idx_of_iter_subtree = self.get_next_step(self.total_list[i])
                stack.append(
                    (self.total_list[i], cur_step, cur_tree, iter_tree, i, idx_of_iter_subtree))
                i = idx_of_iter_subtree
                cur_tree = BlockSchemeTree()
                cur_step = cur_tree
            elif cur_fig == 'HexagonCycleEndPoint':
                cur_cycle = stack.pop()
                cur_step = CycleStep(cur_cycle[0]['code'], '', cur_tree, cur_cycle[1], cur_cycle[2])
                cur_tree = cur_cycle[2]
                i += 1
            else:
                i += 1
        print(self.total_list)

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