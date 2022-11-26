from ..BlockSchemeTree import BlockSchemeTree
from .StepsTypeEnum import StepsTypesEnum


class ConditionStep(BlockSchemeTree):
    def __init__(self, condition_string, yes_tree, no_tree, prev_step, parent_tree):
        super().__init__(prev_step, parent_tree, StepsTypesEnum.FuncStep)
        self.condition_string = condition_string
        self.yes_tree = yes_tree
        self.yes_tree.prev_step = self
        self.no_tree = no_tree
        self.no_tree.prev_step = self

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}if {self.condition_string}:'
        self.yes_tree.level = self.level + 1
        self.yes_tree.initial_step.level = self.level + 1
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.yes_tree.generate_code()}'
        if self.no_tree is not None:
            self.no_tree.level = self.level + 1
            self.no_tree.initial_step.level = self.level + 1
            self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
            self.parent_tree.result_code = f'{self.parent_tree.result_code}else:'
            self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.no_tree.generate_code()}'
