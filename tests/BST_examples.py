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


if __name__ == "__main__":
    examples = [example_hello, example_minimum, example_maximum, example_decrement, example_cycle]
    for example in examples:
        example()
