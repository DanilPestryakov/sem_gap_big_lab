import math
def ConnectElementsAndBoxes(text_file, box_file, coord_file):
    SchemeElements = []
    ft = open(text_file)
    fb = open(box_file)
    fc = open(coord_file)
    text = ft.readlines()
    box = fb.readlines()
    coord = fc.readlines()

    for i in range(len(text)):
        SchemeElements.append({"text": text[i].strip(), "box": box[i].strip(), "coord": coord[i].strip(), "tree": None})

    for elem in SchemeElements:
        elem["box"] = list(map(lambda x: int(x), elem["box"].split()))
        elem["coord"] = list(map(lambda x: int(x), elem["coord"].split()))

    return SchemeElements

def DataStructure(Figure, Text, output_lines_point):

    EPS_DIST = 10

    newlist = sorted(Figure, key=lambda i: i['coord'][1], reverse=False)

    list1 = []  # filtered from circles (program begin/end)
    circle = [d if d['text'] == 'Circle' else list1.append(d) for d in newlist]
    circle = list(filter(lambda item: item is not None, circle))

    newlist_circle = sorted(circle, key=lambda i: i['coord'][1], reverse=False)
    program_begin = newlist_circle[0]
    program_end = newlist_circle[1]

    list2 = []  # filtered from program arguments figure
    arguments = [d if d['text'] == 'Quadrilateral' and
                 math.pow(d['coord'][1] - program_begin['coord'][1], 2) < EPS_DIST else list2.append(d) for d in list1]
    arguments = list(filter(lambda item: item is not None, arguments))
#    print(arguments)
#    print(list2)

    Points = []
    with open(output_lines_point) as f:
        lines = f.readlines()
        for line in lines:
            x, y = list(map(lambda x: int(x), line.split()))
            Points.append([x, y])

#    print(Points)

    hexagon = [d for d in list2 if d['text'] == 'HexagonCondition' or d['text'] == 'HexagonCycle']
#    print(hexagon)

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

    for i in range(len(hexagon)):
        yes_trees_elems.append(hexagon[i])
        no_trees_elems.append(hexagon[i])
        for elem in list2:
            if hexagon[i]['coord'][1] < elem['coord'][1] < Points[i][1] and int(cond_levels[i]*0.9) < elem['coord'][0] < int(cond_levels[i]*1.1):
                yes_trees_elems.append(elem)
            elif hexagon[i]['coord'][1] < elem['coord'][1] < Points[i][1] and int(cond_levels[i]*1.1) < elem['coord'][0] < int(cond_levels[i]*4.0):
                no_trees_elems.append(elem)
            else:
                bst_tree_elems.append(elem)
 #           yes_trees_elems.append(hexagon[i])
 #           no_trees_elems.append(hexagon[i])

    bst_tree_all = bst_tree_elems
    bst_tree_all.append(program_begin)
    bst_tree_all.append(program_end)
    # print('bst_tree_all', bst_tree_all)

    bst_tree = sorted(bst_tree_all, key=lambda i: i['coord'][1], reverse=False)
    yes_trees = sorted(yes_trees_elems, key=lambda i: i['coord'][1], reverse=False)
    no_trees = sorted(no_trees_elems, key=lambda i: i['coord'][1], reverse=False)

#    print('bst_tree_elems', bst_tree_elems)
#    print('program_begin', program_begin)
#    print('program_end', program_end)
#    print('hexagon', hexagon)

    for elem in bst_tree:
        x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
        for code in Text:
            x, y = code['coord']
            if (x0 < x < x1) and (y0 < y < y2):
                elem['code'] = code['text']

    for elem in yes_trees:
        x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
        for code in Text:
            x, y = code['coord']
            if (x0 < x < x1) and (y0 < y < y2):
                elem['code'] = code['text']

    for elem in no_trees:
        x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
        for code in Text:
            x, y = code['coord']
            if (x0 < x < x1) and (y0 < y < y2):
                elem['code'] = code['text']

    for elem in arguments:
        x0, y0, x1, y1, x2, y2, x3, y3 = elem['box']
        elem['code'] = []
        for code in Text:
            x, y = code['coord']
            if (x0 < x < x1) and (y0 < y < y2):
                elem['code'].append(code['text'])


    print('arguments:\n', arguments)
    print('bst_tree:\n', bst_tree)
    print('yes_trees:\n', yes_trees)
    print('no_trees:\n',no_trees)

    # print('Text', Text)
