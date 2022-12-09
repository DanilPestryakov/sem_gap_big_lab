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

def DataStructure(Figure, Text):

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
    print(arguments)
    print(list2)
