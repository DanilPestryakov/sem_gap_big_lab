from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum


class CycleStep(BlockSchemeTree):
    def __init__(self, start_step_string: str, condition_string: str, iterator_string: str,
                 iterable_tree: BlockSchemeTree, prev_step: BlockSchemeTree, parent_tree: BlockSchemeTree):
        """
        Create instance for block scheme tree representation of cycle step in block scheme instance.

        :param start_step_string: string with condition variable initializing
        :param condition_string: string with condition for cycle finish
        :param iterator_string: string with code what need to do with condition variable
        :param iterable_tree: block scheme tree related for steps to need iterate
        :param prev_step: previous step of block scheme
        :param parent_tree: parent tree for this node
        """
        super().__init__(prev_step, parent_tree, StepsTypesEnum.CycleStep)
        self.start_step_string = start_step_string
        self.condition_string = condition_string
        self.iterator_string = iterator_string
        self.iterable_tree = iterable_tree

    def generate_code(self):
        """
        Recursive generation of code for this step
        """

        # generate code for initializing condition variable
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.start_step_string}'
        # generate code for initializing while cycle
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}while {self.condition_string}:'
        # set level of tabulation for iterable tree
        self.iterable_tree.level = self.level + 1
        self.iterable_tree.initial_step.level = self.level + 1
        # recursive generation of code for iterable tree
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.iterable_tree.generate_code()}'
        # generate code for handle condition variable
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * (self.level + 1)
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.iterator_string}'
