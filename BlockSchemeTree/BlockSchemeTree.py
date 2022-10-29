class BlockSchemeTree:
    def __init__(self, initial_step=None):
        self.level = 0
        self.next_step = None
        self.prev_step = None
        self.step_type = ''
        self.initial_step = initial_step

    def generate_code(self):
        if self.initial_step is None:
            print('Define initial step')
        else:
            try:
                curr_step = self.initial_step
                while curr_step.next_step is not None:
                    curr_step.generate_code()
                    curr_step = curr_step.next_step
            except:
                print('Something went wrong')
