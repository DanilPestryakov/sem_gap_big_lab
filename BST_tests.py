from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import ConditionStep, CycleStep, FuncStep, SimpleCodeStep


def test_1():
    print(f"{'_' * 30}\nTest 1")
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('print(a, b)', hello_step, bst)

    bst.set_initial_step(hello_step)
    print(bst.generate_code())


def test_6():
    print(f"{'_' * 30}\nTest 6")
    bst = BlockSchemeTree()
    counter = FuncStep('counter', [], bst, bst)
    iterable_tree = BlockSchemeTree()
    print_step = SimpleCodeStep('print(i)', iterable_tree, iterable_tree)
    iterator_step = CycleStep('i = 1', 'i > 10', 'i = i + 1', iterable_tree, counter, bst)

    iterable_tree.set_initial_step(print_step)
    bst.set_initial_step(counter)
    print(bst.generate_code())


def test_7():
    print(f"{'_' * 30}\nTest 7")
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


if __name__ == "__main__":
    tests = [test_1, test_6, test_7]
    for test in tests:
        test()
