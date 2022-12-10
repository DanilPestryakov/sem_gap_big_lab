from typing import Optional

from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum


class ConditionStep(BlockSchemeTree):
    def __init__(self, condition_string: str, yes_tree: BlockSchemeTree,
                 no_tree: Optional[BlockSchemeTree], prev_step: BlockSchemeTree,
                 parent_tree: BlockSchemeTree):
        """
        Create instance for block scheme tree representation of condition step in block scheme instance.

        :param condition_string: string with condition
        :param yes_tree: block scheme tree related for yes step
        :param no_tree: block scheme tree related for yes step
        :param prev_step: previous step of block scheme
        :param parent_tree: parent tree for this node
        """
        super().__init__(prev_step, parent_tree, StepsTypesEnum.ConditionStep)
        self.condition_string = condition_string
        self.yes_tree = yes_tree
        self.yes_tree.prev_step = self
        self.no_tree = no_tree
        if self.no_tree is not None:
            self.no_tree.prev_step = self

    def generate_code(self):
        """
        Recursive generation of code for this step
        """
        # set tabulation
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        # set string with condition
        self.parent_tree.result_code = f'{self.parent_tree.result_code}if {self.condition_string}:'
        # set level + 1 for tabulation for tree related yes step
        self.yes_tree.level = self.level + 1
        BlockSchemeTree.increase_steps_level(self.yes_tree.initial_step, self.level + 1)
        # recursive generation of code for yes tree
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.yes_tree.generate_code()}'
        # also do same for no tree if no tree represented
        if self.no_tree is not None:
            self.no_tree.level = self.level + 1
            BlockSchemeTree.increase_steps_level(self.no_tree.initial_step, self.level + 1)
            self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
            self.parent_tree.result_code = f'{self.parent_tree.result_code}else:'
            self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.no_tree.generate_code()}'
