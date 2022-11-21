class BlockSchemeTree:
    def __init__(self, prev_step=None, parent_tree=None, step_type=''):
        self.prev_step = prev_step
        self.parent_tree = parent_tree
        self.step_type = step_type
        self.result_code = ''
        self.initial_step = None
        self.level = self.get_level()
        self.next_step = None
        if prev_step is not None:
            self.prev_step.next_step = self

    def set_initial_step(self, initial_step):
        self.initial_step = initial_step

    def generate_code(self):
        if self.initial_step is None:
            print('Define initial step')
        else:
            try:
                curr_step = self.initial_step
                while curr_step is not None:
                    curr_step.generate_code()
                    curr_step = curr_step.next_step
                print(self.result_code)
            except Exception as e:
                print(e)

    def get_level(self):
        from .Steps import StepsTypesEnum

        if self.prev_step is None:
            return 0
        elif self.prev_step.step_type == StepsTypesEnum.FuncStep:
            return self.prev_step.level + 1
        else:
            return self.prev_step.level
