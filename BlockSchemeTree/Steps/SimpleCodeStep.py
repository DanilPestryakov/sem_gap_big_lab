from ..BlockSchemeTree import BlockSchemeTree


class SimpleCodeStep(BlockSchemeTree):
    def __init__(self, code_str, prev_step, parent_tree, step_type):
        super().__init__(prev_step, parent_tree, step_type)
        self.code_str = code_str
        self.parent_tree = parent_tree

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.code_str}'
