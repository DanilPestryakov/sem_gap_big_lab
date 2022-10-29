from BlockSchemeTree import BlockSchemeTree
from BlockSchemeTree.Steps import FuncStep

if __name__ == "__main__":
    bst = BlockSchemeTree()
    hello_step = FuncStep('hello', ['a', 'b=7'], bst, None, bst)
    bst.set_initial_step(hello_step)
    bst.generate_code()
