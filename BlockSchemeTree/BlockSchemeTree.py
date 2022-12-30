from __future__ import annotations

from .StepsTypeEnum import StepsTypesEnum


class BlockSchemeTree:
    def __init__(self, prev_step: BlockSchemeTree = None, parent_tree: BlockSchemeTree = None,
                 step_type: StepsTypesEnum = None):
        """
        Create a block scheme representation tree structure instance.

        :param prev_step: previous step of block scheme
        :param parent_tree: parent tree for this node
        :param step_type: type of current step in Block
        """
        self.prev_step = prev_step
        self.parent_tree = parent_tree
        self.step_type = step_type
        # variable for storing generated code
        self.result_code = ''
        # initial (also start or first) step in tree
        self.initial_step = None
        # level of tabulation
        self.level = self.get_level()
        # next step
        self.next_step = None
        # set next step
        if prev_step is not None:
            self.prev_step.next_step = self
        if prev_step == parent_tree and parent_tree is not None:
            self.parent_tree.initial_step = self

    def set_initial_step(self, initial_step: BlockSchemeTree):
        """
        Set step step in tree

        :param initial_step: first or initial step in tree
        """
        self.initial_step = initial_step

    def generate_code(self) -> str:
        """
        Generate code for current tree
        """
        if self.initial_step is None:
            raise Exception("Set initial step!")
        else:
            try:
                curr_step = self.initial_step
                # recursive generation of code for steps until the steps end
                while curr_step is not None:
                    curr_step.generate_code()
                    curr_step = curr_step.next_step
                return self.result_code
            except Exception as e:
                print(e)

    def get_level(self):
        """
        Get current level of tabulation by step and previous step level
        """
        if self.prev_step is None:
            return 0
        elif self.prev_step.step_type == StepsTypesEnum.FuncStep:
            return self.prev_step.level + 1
        else:
            return self.prev_step.level

    @classmethod
    def increase_steps_level(cls, first_step: BlockSchemeTree, new_level: int):
        """
        Increasing level of subtrees steps
        """
        cur_step = first_step
        while cur_step is not None:
            cur_step.level = new_level
            cur_step = cur_step.next_step
