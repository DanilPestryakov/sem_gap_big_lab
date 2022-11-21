from ..BlockSchemeTree import BlockSchemeTree
from .StepsTypeEnum import StepsTypesEnum


class CycleStep(BlockSchemeTree):
    def __init__(self, start_step_string, condition_string, iterator_string, prev_step, parent_tree):
        super().__init__(prev_step, parent_tree, StepsTypesEnum.CycleStep)
        self.start_step_string = start_step_string
        self.condition_string = condition_string
        self.iterator_string = iterator_string

    def generate_code(self):
        pass
