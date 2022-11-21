from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import FuncStep, SimpleCodeStep, StepsTypesEnum

if __name__ == "__main__":
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b=7'], bst, bst)
    str_1_step = SimpleCodeStep('a = a + b', hello_step, bst)
    str_2_step = SimpleCodeStep('с = a + b', str_1_step, bst)

    bst.set_initial_step(hello_step)
    bst.generate_code()
