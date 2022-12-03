from ..BlockSchemeTree import BlockSchemeTree
from ..StepsTypeEnum import StepsTypesEnum

class ConditionStep(BlockSchemeTree):
    def __init__(self, condition_string, yes_tree, no_tree, prev_step, parent_tree):
        """
        Create a drawing instance.

        :param im: The image to draw in.
        :param mode: Optional mode to use for color values.  For RGB
                   images, this argument can be RGB or RGBA (to blend the
                   drawing into the image).  For all other modes, this argument
                   must be the same as the image mode.  If omitted, the mode
                   defaults to the mode of the image.
        """
        super().__init__(prev_step, parent_tree, StepsTypesEnum.FuncStep)
        self.condition_string = condition_string
        self.yes_tree = yes_tree
        self.yes_tree.prev_step = self
        self.no_tree = no_tree
        self.no_tree.prev_step = self

    def generate_code(self):
        """
            Gets the "base" mode for given mode.  This function returns "L" for
            images that contain grayscale data, and "RGB" for images that
            contain color data.

        :param mode: Input mode.
        :returns: "L" or "RGB".
        :exception KeyError: If the input mode was not a standard mode.
        """
        self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
        self.parent_tree.result_code = f'{self.parent_tree.result_code}if {self.condition_string}:'
        self.yes_tree.level = self.level + 1
        self.yes_tree.initial_step.level = self.level + 1
        self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.yes_tree.generate_code()}'
        if self.no_tree is not None:
            self.no_tree.level = self.level + 1
            self.no_tree.initial_step.level = self.level + 1
            self.parent_tree.result_code = f'{self.parent_tree.result_code}\n' + '\t' * self.level
            self.parent_tree.result_code = f'{self.parent_tree.result_code}else:'
            self.parent_tree.result_code = f'{self.parent_tree.result_code}{self.no_tree.generate_code()}'
