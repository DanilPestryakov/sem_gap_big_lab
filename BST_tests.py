from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import ConditionStep, FuncStep, SimpleCodeStep


def test_1():
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b'], bst, bst)
    str_1_step = SimpleCodeStep('print(a, b)', hello_step, bst)

    bst.set_initial_step(hello_step)
    print(bst.generate_code())


def test_2():
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
    test_1()
    test_2()
