from typing import List

from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum


class FuncStep(BlockSchemeTree):
    def __init__(self, func_name: str, args_string: List[str], prev_step: BlockSchemeTree,
                 parent_tree: BlockSchemeTree):
        """
        Create instance for block scheme tree representation of func step in block scheme instance.

        :param func_name: name of function
        :param args_string: list of strings with function arguments
        :param prev_step: previous step of block scheme
        :param parent_tree: parent tree for this node
        """
        super().__init__(prev_step, parent_tree, StepsTypesEnum.FuncStep)
        self.func_name = func_name
        self.args_string = args_string
        self.parent_tree = parent_tree

    def generate_code(self):
        """
        Generation of code for this step
        """
        # set tabulation
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        # sort args and kwargs
        sorted_args_strings = sorted(self.args_string, key=lambda x: "=" in x)
        # generate code for function definition
        self.parent_tree.result_code = f'{self.parent_tree.result_code}def {self.func_name}' \
                                       f'({", ".join(sorted_args_strings)}):'
