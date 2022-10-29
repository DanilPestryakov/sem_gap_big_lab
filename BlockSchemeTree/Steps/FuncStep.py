from ..BlockSchemeTree import BlockSchemeTree


class FuncStep(BlockSchemeTree):
    def __init__(self, func_name, args_string, next_step, prev_step):
        super(BlockSchemeTree, self).__init__()
        self.func_name = func_name
        self.args_string = args_string
        self.next_step = next_step
        self.prev_step = prev_step
        self.level = self.prev_step.level

    def generate_code(self):
        self.result_code = f'{self.result_code}\n' + '\t' * self.level
        sorted_args_strings = sorted(self.args_string.sort(key=lambda x: "=" in x))
        self.result_code = f'{self.result_code}{self.func_name}' \
                           f'({", ".join(sorted_args_strings)})'
