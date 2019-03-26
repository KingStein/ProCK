import math

from kicker.model_game_bar import GameBar
from kicker.CONST_GAME_FIGURES import *
from kicker.CONST_BALL import Coordinate
from kicker.CONST_SIMULATION import SIMULATION_TIME_STEP
from kicker.CONST_SIMULATION import SHOOT_SPEED
from kicker.CONST_SIMULATION import BAR_SPEED
from kicker.CONST_KICKER import COURT_HEIGHT


class Generic_Game_Bar:
    X_REFLECTION_PLANE = self.x + FIGURE_FOOT_WIDTH + BALL_RADIUS

    def __init__(self, x_position):   # position defines the kind of bar (keeper, defender etc..)
        self.intersection = 0
        self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
        self.x_position = x_position
        self.next_position = -1
        self.figures_position = []

        if x_position == BAR_POSITION_KEEPER_COMPUTER:
            self.max_travel_length = MAX_POS_KEEPER
            self.y_position = MAX_POS_KEEPER / 2
            self.distance_between_figures = 0
            self.figures_position = [POSITION_ON_BAR_KEEPER_COMPUTER]

        elif x_position == BAR_POSITION_DEFENDER_COMPUTER:
            self.max_travel_length = MAX_POS_DEFENDER
            self.y_position = MAX_POS_DEFENDER / 2
            self.distance_between_figures = DEFENDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_DEFENDER_RIGHT_COMPUTER,
                                     POSITION_ON_BAR_DEFENDER_LEFT_COMPUTER
                                     ]

        elif x_position == BAR_POSITION_MIDFIELDER_COMPUTER:
            self.max_travel_length = MAX_POS_MIDFIELDER
            self.y_position = MAX_POS_MIDFIELDER / 2
            self.distance_between_figures = MIDFIELDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_MIDFIELDER_LEFT_OUTSIDE_COMPUTER,
                                     POSITION_ON_BAR_MIDFIELDER_LEFT_COMPUTER,
                                     POSITION_ON_BAR_MIDFIELDER_MIDDLE_COMPUTER,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_COMPUTER,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_OUTSIDE_COMPUTER
                                     ]

        elif x_position == BAR_POSITION_FORWARD_COMPUTER:
            self.max_travel_length = MAX_POS_FORWARD
            self.y_position = MAX_POS_FORWARD / 2
            self.distance_between_figures = FORWARD_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_FORWARD_LEFT_COMPUTER,
                                     POSITION_ON_BAR_FORWARD_MIDDLE_COMPUTER,
                                     POSITION_ON_BAR_FORWARD_RIGHT_COMPUTER
                                     ]


        elif x_position == BAR_POSITION_KEEPER_HUMAN:
            self.max_travel_length = MAX_POS_KEEPER
            self.y_position = MAX_POS_KEEPER / 2
            self.distance_between_figures = 0
            self.figures_position = [POSITION_ON_BAR_KEEPER_HUMAN]

        elif x_position == BAR_POSITION_DEFENDER_HUMAN:
            self.max_travel_length = MAX_POS_DEFENDER
            self.y_position = MAX_POS_DEFENDER / 2
            self.distance_between_figures = DEFENDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_DEFENDER_RIGHT_HUMAN,
                                     POSITION_ON_BAR_DEFENDER_LEFT_HUMAN
                                     ]

        elif x_position == BAR_POSITION_MIDFIELDER_HUMAN:
            self.max_travel_length = MAX_POS_MIDFIELDER
            self.y_position = MAX_POS_MIDFIELDER / 2
            self.distance_between_figures = MIDFIELDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_MIDFIELDER_LEFT_OUTSIDE_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_LEFT_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_MIDDLE_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_OUTSIDER_HUMAN
                                     ]

        elif x_position == BAR_POSITION_FORWARD_HUMAN:
            self.max_travel_length = MAX_POS_FORWARD
            self.y_position = MAX_POS_FORWARD / 2
            self.distance_between_figures = FORWARD_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_FORWARD_LEFT_HUMAN
                                     POSITION_ON_BAR_FORWARD_MIDDLE_HUMAN
                                     POSITION_ON_BAR_FORWARD_RIGHT_HUMAN
                                     ]


    def check_for_shoot(self, kicker):
        shoot = False
        intersection = kicker.ball.pos[Coordinate.Y] - math.tan(kicker.ball.angle) * \
                       (kicker.ball.pos[Coordinate.X] - self.x_reflectioin_plane)

        for figure in self.figures_position:
            if self.y_position + figure - Y_OFFSET_REFLECTION_PLANE < intersection \
                    < self.y_position + figure + Y_OFFSET_REFLECTION_PLANE:
                self.shoot(kicker, intersection, TeamHuman.DEFENDER_RIGHT)
                shoot = True
                break

        return shoot

    def move_bar(self):
        def calc_v(direction):
            v = self.v_bar - BAR_ACC * SIMULATION_TIME_STEP * direction
            if abs(v) > BAR_SPEED:
                v = BAR_SPEED * -direction
            return v

        def calc_new_pos(direction):
            return self.position + self.v_bar * SIMULATION_TIME_STEP - 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP) * direction

        self.next_position = round(self.next_position)
        #self.position = round(self.position)
        if self.next_position != round(self.position):
            if 0 <= self.next_position <= self.max_forward:

                if self.next_position > self.position:
                    direction = -1 * self.stop_flag
                else:
                    direction = 1 * self.stop_flag

                new_temp_pos = calc_new_pos(direction)
                self.v_bar = calc_v(direction)

                x_stop = (self.v_bar * self.v_bar) / (2 * BAR_ACC)

                if abs(self.next_position - new_temp_pos) < x_stop:
                    if(self.v_bar == 0):
                        new_temp_pos = self.next_position
                    self.stop_flag = -1
                    self.position = new_temp_pos
                    if new_temp_pos > self.next_position:
                        self.position = self.next_position

                else:

                    if self.v_bar < BAR_SPEED * direction:
                        if self.v_bar >= BAR_SPEED * direction:
                            self.v_bar = BAR_SPEED *direction

                self.position = new_temp_pos

            else:
                self.next_position = -1
                self.v_bar = 0
        else:
            self.next_position = -1
            self.v_bar = 0


     def reset_bar(self):
        self.next_position = -1
        self.y_position = self.max_travel_length / 2
        self.v_bar = 0
        self.stop_flag = 1
