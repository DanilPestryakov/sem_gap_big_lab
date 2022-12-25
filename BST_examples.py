from typing import Tuple, List

from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import ConditionStep, CycleStep, FuncStep, SimpleCodeStep
from DataStructureConnector import *


def example_hello():
    print(f"{'_' * 30}\nExample hello")
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('print(a, b)', hello_step, bst)

    print(bst.generate_code())


def example_minimum():
    print(f"{'_' * 30}\nExample minimum")
    bst = BlockSchemeTree()
    minimum = FuncStep('minimum', ['a=7', 'b=3'], bst, bst)
    yes_tree = BlockSchemeTree()
    no_tree = BlockSchemeTree()
    yes_step = SimpleCodeStep('print(a)', yes_tree, yes_tree)
    no_step = SimpleCodeStep('print(b)', no_tree, no_tree)
    cond = ConditionStep('a < b', yes_tree, no_tree, minimum, bst)

    print(bst.generate_code())


def example_maximum():
    print(f"{'_' * 30}\nExample maximum")
    bst = BlockSchemeTree()
    maximum = FuncStep('maximum', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('c = a', maximum, bst)
    yes_tree = BlockSchemeTree()
    yes_step = SimpleCodeStep('c = b', yes_tree, yes_tree)
    cond = ConditionStep('b > a', yes_tree, None, str_1_step, bst)
    str_2_step = SimpleCodeStep('print(c)', cond, bst)

    print(bst.generate_code())


def example_decrement():
    print(f"{'_' * 30}\nExample decrement")
    bst = BlockSchemeTree()
    decrement = FuncStep('decrement', ["a=7", "b=3"], bst, bst)
    iterable_tree = BlockSchemeTree()
    iterable_step = SimpleCodeStep('a = a - 1', iterable_tree, iterable_tree)
    iterator_step = CycleStep('a > b', '', iterable_tree, decrement, bst)

    print_step = SimpleCodeStep('print(a)', iterator_step, bst)

    print(bst.generate_code())


def example_cycle():
    print(f"{'_' * 30}\nExample cycle")
    bst = BlockSchemeTree()
    cycle = FuncStep('cycle', [], bst, bst)
    iterable_tree = BlockSchemeTree()
    iterable_step = SimpleCodeStep('print(i)', iterable_tree, iterable_tree)
    iterator_step = CycleStep('for i in range (1, 11)', '', iterable_tree, cycle, bst)

    print(bst.generate_code())


def MyTest():
    print(f"{'_' * 30}\nMy example")
    bst = BlockSchemeTree()
    maximum = FuncStep('JustSoTest', ['a', 'b'], bst, bst)

    str_1_step = SimpleCodeStep('a = a', maximum, bst)
    str_2_step = SimpleCodeStep('b = b', str_1_step, bst)

    yes_tree = BlockSchemeTree()

    yes_step1 = SimpleCodeStep('yes = yes', yes_tree, yes_tree)
    yes_step2 = SimpleCodeStep('yes!', yes_step1, yes_tree)

    no_tree1 = BlockSchemeTree()
    str_n1_step = SimpleCodeStep('print(d)', no_tree1, no_tree1)
    str_n2_step = SimpleCodeStep('print(F)', str_n1_step, no_tree1)

    yes_tree1 = BlockSchemeTree()
    str_y1_step = SimpleCodeStep('print(ddd)', yes_tree1, yes_tree1)
    str_y2_step = SimpleCodeStep('print(FFF)', str_y1_step, yes_tree1)

    cond1 = ConditionStep('c > d', yes_tree1, no_tree1, yes_step2, yes_tree)

    cond = ConditionStep('b > a', yes_tree, None, str_2_step, bst)

    str_3_step = SimpleCodeStep('print(c)', cond, bst)

    print(bst.generate_code())


def MyTest2():
    print(f"{'_' * 30}\nMy example")
    bst = BlockSchemeTree()
    maximum = FuncStep('JustSoTest', ['a', 'b'], bst, bst)

    str_1_step = SimpleCodeStep('a = a', maximum, bst)
    str_2_step = SimpleCodeStep('b = b', str_1_step, bst)

    yes_tree = BlockSchemeTree()
    yes_step1 = SimpleCodeStep('yes = yes', yes_tree, yes_tree)
    yes_step2 = SimpleCodeStep('yes!', yes_step1, yes_tree)

    no_tree1 = BlockSchemeTree()
    str_n1_step = SimpleCodeStep('print(d)', no_tree1, no_tree1)
    str_n2_step = SimpleCodeStep('print(F)', str_n1_step, no_tree1)

    yes_tree1 = BlockSchemeTree()
    str_y1_step = SimpleCodeStep('print(ddd)', yes_tree1, yes_tree1)
    str_y2_step = SimpleCodeStep('print(FFF)', str_y1_step, yes_tree1)

    cond = ConditionStep('b > a', yes_tree, None, str_2_step, bst)
    cond1 = ConditionStep('c > d', yes_tree1, no_tree1, cond, bst)

    str_3_step = SimpleCodeStep('print(c)', cond1, bst)

    print(bst.generate_code())


def has_neighbour_yes(scheme: List[dict], elem: dict) -> Tuple[dict, int]:
    for num, item in enumerate(scheme):
        dist_x = abs(elem['coord'][0] - item['coord'][0])
        dist_y = item['coord'][1] - elem['coord'][1]
        if dist_x < 10 and 0 < dist_y < 100:
            return item, num
    return {}, 0


def get_next_step(scheme: List[dict], elem: dict) -> Tuple[dict, int]:
    return has_neighbour_yes(scheme, elem)


def has_neighbour_no(scheme: List[dict], elem: dict) -> Tuple[dict, int]:
    for num, item in enumerate(scheme):
        dist_x = item['coord'][0] - elem['coord'][0]
        dist_y = item['coord'][1] - elem['coord'][1]
        if 200 < dist_x < 400 and 0 < dist_y < 100:
            return item, num
    return {}, 0


def DataStructureExample(SCHEME):
    print(f"{'_' * 30}\nExample minimum with DataStructure")

    print(SCHEME)

    SCHEME_SORT = sorted(SCHEME, key=lambda f: f['coord'][1], reverse=False)

    cycles_begin = [d for d in SCHEME_SORT if d['text'] == 'HexagonCondition' \
                    or d['text'] == 'HexagonCycle' or d['text'] == 'Circle']
    cycles_end = [d for d in SCHEME_SORT if d['text'] == 'EndPoint' or d['text'] == 'CircleEndPoint' \
                  or d['text'] == 'HexagonCycleEndPoint']

    for hexagon in cycles_begin:
        print('hexagon =', hexagon)
        yes_n, num = has_neighbour_yes(SCHEME_SORT, hexagon)
        print(f'yes_n = {yes_n}, num = {num}')
        no_n, num = has_neighbour_no(SCHEME_SORT, hexagon)
        print(f'no_n = {no_n}, num = {num}')

    levels = sorted(cycles_begin, key=lambda b: b['coord'][0], reverse=False)


#   print()
#   print(cycles_begin)
#   print()
#   print(cycles_end)
#   print()
#   print(levels)

#    bst = BlockSchemeTree()

#    if arguments:
#        programe_name = FuncStep(BST_TREE[0][0]['code'], arguments[0]['code'], bst, bst)
#    else:
#        programe_name = FuncStep(BST_TREE[0][0]['code'], '', bst, bst)

#    if NO_TREES and len(NO_TREES[0]) > 1:
#        yes_tree = [BlockSchemeTree()]*len(YES_TREES)
#        no_tree = [BlockSchemeTree()] * len(NO_TREES)
#        for i in range(len(YES_TREES)):
#            init_step_yes = SimpleCodeStep(YES_TREES[i][1]['code'], yes_tree[i], yes_tree[i])
#            init_step_no = SimpleCodeStep(NO_TREES[i][1]['code'], no_tree[i], no_tree[i])
#            yes_tree[i].set_initial_step(init_step_yes)
#            no_tree[i].set_initial_step(init_step_no)
#            cond = ConditionStep(YES_TREES[i][0]['code'], yes_tree[i], no_tree[i], programe_name, bst)
#    elif YES_TREES and len(YES_TREES[0]) > 1:
#        yes_tree = [BlockSchemeTree()]*len(YES_TREES)
#        for i in range(len(YES_TREES)):
#            init_step_yes = SimpleCodeStep(YES_TREES[i][1]['code'], yes_tree[i], yes_tree[i])
#            yes_tree[i].set_initial_step(init_step_yes)
#            cond = ConditionStep(YES_TREES[i][0]['code'], yes_tree[i], None, programe_name, bst)

#    bst.set_initial_step(programe_name)
#    print(bst.generate_code())


if __name__ == "__main__":
    # examples = [example_hello, example_minimum, example_maximum, example_decrement, example_cycle, MyTest]
    # examples = [MyTest, MyTest2]
    examples = [DataStructureExample]
    for example in examples:
        example()
