import math

from kicker.model_game_bar import GameBar
from kicker.CONST_GAME_FIGURES import *
from kicker.CONST_BALL import Coordinate
from kicker.CONST_SIMULATION import *

from kicker.CONST_KICKER import COURT_HEIGHT


class Generic_Game_Bar:

    def __init__(self, x_position):   # position defines the kind of bar (keeper, defender etc..)
        self.intersection = 0
        self.x_position = x_position
        self.next_position = -1
        self.figures_position = []
        self.v_bar = 0

        if x_position == BAR_POSITION_KEEPER_COMPUTER:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_KEEPER
            self.y_position = MAX_POS_KEEPER / 2
            self.distance_between_figures = 0
            self.figures_position = [POSITION_ON_BAR_KEEPER_COMPUTER]

        elif x_position == BAR_POSITION_DEFENDER_COMPUTER:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_DEFENDER
            self.y_position = MAX_POS_DEFENDER / 2
            self.distance_between_figures = DEFENDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_DEFENDER_RIGHT_COMPUTER,
                                     POSITION_ON_BAR_DEFENDER_LEFT_COMPUTER
                                     ]

        elif x_position == BAR_POSITION_MIDFIELDER_COMPUTER:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
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
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_FORWARD
            self.y_position = MAX_POS_FORWARD / 2
            self.distance_between_figures = FORWARD_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_FORWARD_LEFT_COMPUTER,
                                     POSITION_ON_BAR_FORWARD_MIDDLE_COMPUTER,
                                     POSITION_ON_BAR_FORWARD_RIGHT_COMPUTER
                                     ]


        elif x_position == BAR_POSITION_KEEPER_HUMAN:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_KEEPER
            self.y_position = MAX_POS_KEEPER / 2
            self.distance_between_figures = 0
            self.figures_position = [POSITION_ON_BAR_KEEPER_HUMAN]

        elif x_position == BAR_POSITION_DEFENDER_HUMAN:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_DEFENDER
            self.y_position = MAX_POS_DEFENDER / 2
            self.distance_between_figures = DEFENDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_DEFENDER_RIGHT_HUMAN,
                                     POSITION_ON_BAR_DEFENDER_LEFT_HUMAN
                                     ]

        elif x_position == BAR_POSITION_MIDFIELDER_HUMAN:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_MIDFIELDER
            self.y_position = MAX_POS_MIDFIELDER / 2
            self.distance_between_figures = MIDFIELDER_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_MIDFIELDER_LEFT_OUTSIDE_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_LEFT_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_MIDDLE_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_HUMAN,
                                     POSITION_ON_BAR_MIDFIELDER_RIGHT_OUTSIDE_HUMAN
                                     ]

        elif x_position == BAR_POSITION_FORWARD_HUMAN:
            self.x_reflection_plane = self.x_position + FIGURE_FOOT_WIDTH + BALL_RADIUS
            self.max_travel_length = MAX_POS_FORWARD
            self.y_position = MAX_POS_FORWARD / 2
            self.distance_between_figures = FORWARD_DISTANCE_BETWEEN_FIGURES
            self.figures_position = [POSITION_ON_BAR_FORWARD_LEFT_HUMAN,
                                     POSITION_ON_BAR_FORWARD_MIDDLE_HUMAN,
                                     POSITION_ON_BAR_FORWARD_RIGHT_HUMAN
                                     ]


    def check_for_interaction(self, kicker):
        if kicker.ball.pos[Coordinate.X] > self.x_reflection_plane:
            if kicker.ball.pos[Coordinate.X] - self.x_reflection_plane <= (kicker.ball.pos[Coordinate.X] -
                                                                           kicker.ball.new_pos[Coordinate.X]):
                shoot = self.check_for_shoot(kicker)
            else:
                shoot = False

            side_collision = False
        elif self.x_reflection_plane - kicker.ball.pos[Coordinate.X] < (kicker.ball.speed * SIMULATION_TIME_STEP +
                                                                        X_OFFSET_REFLECTION_PLANE):
            side_collision = self.check_for_side_collision(kicker)
            shoot = False
        else:
            side_collision = False
            shoot = False
        return shoot, side_collision


    def check_for_sidecollision(self, kicker):
        if kicker.ball.angle > 0:       # check if ball hits lower part of figure foot
            for figure in self.figures_position:
                if kicker.ball.pos[Coordinate.Y] < (self.y_position + figure - Y_OFFSET_REFLECTION_PLANE) < kicker.ball.new_pos[Coordinate.Y]:
                    intersection = kicker.ball.pos[Coordinate.X] + (self.y_position + figure - Y_OFFSET_REFLECTION_PLANE - kicker.ball.pos[Coordinate.Y]) / math.tan(kicker.ball.angle)
                    if self.x_position < intersection < self.x_position + X_OFFSET_REFLECTION_PLANE:
                        delta_t_collision = (self.y_position + figure -Y_OFFSET_REFLECTION_PLANE - kicker.ball.pos[Coordinate.Y]) / (math.sin(kicker.ball.angle) * kicker.ball.speed)
                        kicker.ball.new_angle = - kicker.ball.angle
                        kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                             kicker.ball.speed * SIMULATION_TIME_STEP)
                        kicker.ball.new_pos[Coordinate.Y] = (self.position + figure -Y_OFFSET_REFLECTION_PLANE + math.sin(kicker.ball.new_angle) * kicker.ball.speed * (SIMULATION_TIME_STEP - delta_t_collision))
                        side_collision = True
                        break
                    else:
                        side_collision = False

        elif kicker.ball.angle < 0:     # check if ball hits upper part of figure
            for figure in self.figures_position:
                if kicker.ball.pos[Coordinate.Y] > (self.y_position + figure + Y_OFFSET_REFLECTION_PLANE) > kicker.ball.new_pos[Coordinate.Y]:
                    intersection = kicker.ball.pos[Coordinate.X] + (kicker.ball.pos[Coordinate.Y] - self.y_position - figure - Y_OFFSET_REFLECTION_PLANE) / math.tan(kicker.ball.angle)
                    if self.x_position < intersection < self.x_position + X_OFFSET_REFLECTION_PLANE:
                        delta_t_collision = (kicker.ball.pos[Coordinate.Y] - self.y_position - figure - Y_OFFSET_REFLECTION_PLANE) / (math.sin(kicker.ball.angle) * kicker.ball.speed)
                        kicker.ball.new_angle = - kicker.ball.angle
                        kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                             kicker.ball.speed * SIMULATION_TIME_STEP)
                        kicker.ball.new_pos[Coordinate.Y] = (self.y_position + figure + Y_OFFSET_REFLECTION_PLANE + math.sin(kicker.ball.new_angle) * kicker.ball.speed * (SIMULATION_TIME_STEP - delta_t_collision))
                        side_collision = True
                        break
                    else:
                        side_collision = False




    def check_for_shoot(self, kicker):
        shoot = False
        intersection = kicker.ball.pos[Coordinate.Y] - math.tan(kicker.ball.angle) * (kicker.ball.pos[Coordinate.X] - self.x_reflection_plane)

        for figure in self.figures_position:
            if self.y_position + figure - Y_OFFSET_REFLECTION_PLANE < intersection < self.y_position + figure + Y_OFFSET_REFLECTION_PLANE:
                self.shoot(kicker, intersection, figure)
                shoot = True
                break
        return shoot

    def shoot(self, kicker, intersection, figure):
        delta_t_collision = (kicker.ball.pos[Coordinate.X] - self.x_reflection_plane) / (math.cos(kicker.ball.angle) * kicker.ball.speed)
        # figure = position of figure on bar as defined in init
        shoot_offset = self.y_position + figure - intersection
        kicker.ball.new_angle = ((math.pi / 3) * (- shoot_offset / (FIGURE_FOOT_HEIGHT / 2 + BALL_RADIUS)))
        kicker.ball.speed = SHOOT_SPEED
        kicker.ball.new_pos[Coordinate.Y] = (intersection + math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                             (SIMULATION_TIME_STEP - delta_t_collision))
        kicker.ball.new_pos[Coordinate.X] = (self.x_reflection_plane + math.cos(kicker.ball.new_angle) *
                                             kicker.ball.speed * (SIMULATION_TIME_STEP - delta_t_collision))

    def move_bar(self):
        def calc_v(direction):
            v = self.v_bar - BAR_ACC * SIMULATION_TIME_STEP * direction
            if abs(v) > BAR_SPEED:
                v = BAR_SPEED * -direction
            return v

        def calc_new_pos(direction):
            return self.y_position + self.v_bar * SIMULATION_TIME_STEP - 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP) * direction

        self.next_position = round(self.next_position)
        #self.position = round(self.position)
        if self.next_position != round(self.y_position):
            if 0 <= self.next_position <= self.max_travel_length:

                if self.next_position > self.y_position:
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

                self.y_position = new_temp_pos

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
