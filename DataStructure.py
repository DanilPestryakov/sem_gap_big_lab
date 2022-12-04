
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

    newlist = sorted(Figure, key=lambda i: i['coord'][1], reverse=False)
    print(newlist)
    circle = [d for d in newlist if d['text'] == 'Circle']
    print(circle)
    newlist_circle = sorted(circle, key=lambda i: i['coord'][1], reverse=False)
    print(newlist_circle)
