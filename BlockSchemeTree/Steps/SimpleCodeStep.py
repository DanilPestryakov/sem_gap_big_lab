from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum


class SimpleCodeStep(BlockSchemeTree):
    def __init__(self, code_str, prev_step, parent_tree):
        super().__init__(prev_step, parent_tree, StepsTypesEnum.SimpleCodeStep)
        self.code_str = code_str
        self.parent_tree = parent_tree

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.code_str}'
