from ..BlockSchemeTree import BlockSchemeTree
from .StepsTypeEnum import StepsTypesEnum


class CycleStep(BlockSchemeTree):
    def __init__(self, start_step_string, condition_string, iterator_string, iterable_tree, prev_step, parent_tree):
        super().__init__(prev_step, parent_tree, StepsTypesEnum.CycleStep)
        self.start_step_string = start_step_string
        self.condition_string = condition_string
        self.iterator_string = iterator_string
        self.iterable_tree = iterable_tree

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.start_step_string}'
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}while {self.condition_string}:'
        self.iterable_tree.level = self.level + 1
        self.iterable_tree.initial_step.level = self.level + 1
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.iterable_tree.generate_code()}'
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * (self.level + 1)
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.iterator_string}'
