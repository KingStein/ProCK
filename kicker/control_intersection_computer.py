import math

from kicker.model_computer_forward import ComputerForward


class IntersectionStrategy:

    def __init__(self, kicker):
        self.kicker = kicker

    def next_move(self):
        if self.kicker.computer_forward.flag_right:
            new_pos_forward = self.kicker.computer_forward.intersection_FORWARD - ComputerForward.POSITION_ON_BAR_FORWARD_RIGHT


        elif self.kicker.computer_forward.flag_middle:
            new_pos_forward = self.kicker.computer_forward.intersection_FORWARD - ComputerForward.POSITION_ON_BAR_FORWARD_MIDDLE


        elif self.kicker.computer_forward.flag_left:
            new_pos_forward = self.kicker.computer_forward.intersection_FORWARD - ComputerForward.POSITION_ON_BAR_FORWARD_LEFT

        else:
            new_pos_forward = -1

        self.kicker.computer_forward.next_position = new_pos_forward
        self.kicker.computer_forward.move_bar()
