from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import ConditionStep, CycleStep, FuncStep, SimpleCodeStep


def example_hello():
    print(f"{'_' * 30}\nExample hello")
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('print(a, b)', hello_step, bst)

    bst.set_initial_step(hello_step)
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

    yes_tree.set_initial_step(yes_step)
    no_tree.set_initial_step(no_step)
    bst.set_initial_step(minimum)
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

    yes_tree.set_initial_step(yes_step)
    bst.set_initial_step(maximum)
    print(bst.generate_code())


def example_decrement():
    print(f"{'_' * 30}\nExample decrement")
    bst = BlockSchemeTree()
    decrement = FuncStep('decrement', ["a=7", "b=3"], bst, bst)
    iterable_tree = BlockSchemeTree()
    iterable_step = SimpleCodeStep('a = a - 1', iterable_tree, iterable_tree)
    iterator_step = CycleStep('a > b', '', iterable_tree, decrement, bst)

    print_step = SimpleCodeStep('print(a)', iterator_step, bst)

    iterable_tree.set_initial_step(iterable_step)
    bst.set_initial_step(decrement)
    print(bst.generate_code())


def example_cycle():
    print(f"{'_' * 30}\nExample cycle")
    bst = BlockSchemeTree()
    cycle = FuncStep('cycle', [], bst, bst)
    iterable_tree = BlockSchemeTree()
    iterable_step = SimpleCodeStep('print(i)', iterable_tree, iterable_tree)
    iterator_step = CycleStep('for i in range (1, 11)', '', iterable_tree, cycle, bst)

    iterable_tree.set_initial_step(iterable_step)
    bst.set_initial_step(cycle)
    print(bst.generate_code())


def MyTest():
    print(f"{'_' * 30}\nMy example")
    bst = BlockSchemeTree()
    maximum = FuncStep('JustSoTest', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('a = a', maximum, bst)
    str_2_step = SimpleCodeStep('b = b',  str_1_step, bst)

    yes_tree = BlockSchemeTree()
    yes_step1 = SimpleCodeStep('yes = yes', yes_tree, yes_tree)
    yes_step2 = SimpleCodeStep('yes!', yes_step1, yes_tree)

    cond = ConditionStep('b > a', yes_tree, None, str_2_step, bst)
    str_3_step = SimpleCodeStep('print(c)', cond, bst)

    bst.set_initial_step(maximum)
    yes_tree.set_initial_step(yes_step1)

    print(bst.generate_code())

def DataStructureExample(arguments, BST_TREE, YES_TREES, NO_TREES):

    print(f"{'_' * 30}\nExample minimum with DataStructure")
    bst = BlockSchemeTree()

    if arguments:
        programe_name = FuncStep(BST_TREE[0][0]['code'], arguments[0]['code'], bst, bst)
    else:
        programe_name = FuncStep(BST_TREE[0][0]['code'], '', bst, bst)

    if NO_TREES and len(NO_TREES[0]) > 1:
        yes_tree = [BlockSchemeTree()]*len(YES_TREES)
        no_tree = [BlockSchemeTree()] * len(NO_TREES)
        for i in range(len(YES_TREES)):
            init_step_yes = SimpleCodeStep(YES_TREES[i][1]['code'], yes_tree[i], yes_tree[i])
            init_step_no = SimpleCodeStep(NO_TREES[i][1]['code'], no_tree[i], no_tree[i])
            yes_tree[i].set_initial_step(init_step_yes)
            no_tree[i].set_initial_step(init_step_no)
            cond = ConditionStep(YES_TREES[i][0]['code'], yes_tree[i], no_tree[i], programe_name, bst)
    elif YES_TREES and len(YES_TREES[0]) > 1:
        yes_tree = [BlockSchemeTree()]*len(YES_TREES)
        for i in range(len(YES_TREES)):
            init_step_yes = SimpleCodeStep(YES_TREES[i][1]['code'], yes_tree[i], yes_tree[i])
            yes_tree[i].set_initial_step(init_step_yes)
            cond = ConditionStep(YES_TREES[i][0]['code'], yes_tree[i], None, programe_name, bst)

    bst.set_initial_step(programe_name)
    print(bst.generate_code())


if __name__ == "__main__":
    examples = [example_hello, example_minimum, example_maximum, example_decrement, example_cycle, MyTest]
    for example in examples:
        example()
