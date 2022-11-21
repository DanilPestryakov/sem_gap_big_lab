from ..BlockSchemeTree import BlockSchemeTree
from .StepsTypeEnum import StepsTypesEnum


class ConditionStep(BlockSchemeTree):
    def __init__(self, condition_string, yes_step, no_step, prev_step, parent_tree):
        super().__init__(prev_step, parent_tree, StepsTypesEnum.FuncStep)
        self.condition_string = condition_string
        self.yes_step = yes_step
        self.no_step = no_step

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}if {self.condition_string}:\n'
        self.yes_step.level = self.level + 1
        self.no_step.level = self.level + 1
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.yes_step.generate_code()}\n'
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}else:\n'
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.no_step.generate_code()}'
