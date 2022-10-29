from ..BlockSchemeTree import BlockSchemeTree


class FuncStep(BlockSchemeTree):
    def __init__(self, func_name, args_string, prev_step, next_step, parent_tree):
        super(BlockSchemeTree, self).__init__()
        self.func_name = func_name
        self.args_string = args_string
        self.next_step = next_step
        self.prev_step = prev_step
        self.level = self.prev_step.level
        self.parent_tree = parent_tree

    def generate_code(self):
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        sorted_args_strings = sorted(self.args_string, key=lambda x: "=" in x)
        self.parent_tree.result_code = f'{self.parent_tree.result_code}def {self.func_name}' \
                                       f'({", ".join(sorted_args_strings)}):'
