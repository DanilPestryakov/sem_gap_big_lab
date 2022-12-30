from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum


class SimpleCodeStep(BlockSchemeTree):
    def __init__(self, code_str: str, prev_step: BlockSchemeTree, parent_tree: BlockSchemeTree):
        """
        Create instance for block scheme tree representation of simple code step in block scheme instance.

        :param code_str: string of code what need to be execute
        :param prev_step: previous step of block scheme
        :param parent_tree: parent tree for this node
        """
        super().__init__(prev_step, parent_tree, StepsTypesEnum.SimpleCodeStep)
        self.code_str = code_str
        self.parent_tree = parent_tree

    def generate_code(self):
        """
        Generation of code for this step
        """
        # set tabulation
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        # add code string to result code
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.code_str}'
