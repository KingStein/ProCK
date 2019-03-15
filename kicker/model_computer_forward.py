import math

from kicker.model_game_bar import GameBar
from kicker.CONST_GAME_FIGURES import *
from kicker.CONST_BALL import Coordinate
from kicker.CONST_SIMULATION import SIMULATION_TIME_STEP
from kicker.CONST_SIMULATION import SHOOT_SPEED
from kicker.CONST_SIMULATION import BAR_SPEED
from kicker.CONST_SIMULATION import BAR_ACC
from kicker.CONST_KICKER import COURT_HEIGHT


class ComputerForward(GameBar):
    """Konstanten"""
    NUMBER_OF_FIGURES = 3
    DISTANCE_FIGURES = FORWARD_DISTANCE_BETWEEN_FIGURES
    POSITION_ON_BAR_FORWARD_RIGHT = (COURT_HEIGHT - MAX_POS_FORWARD - 2 * DISTANCE_FIGURES) / 2
    POSITION_ON_BAR_FORWARD_MIDDLE = (COURT_HEIGHT - MAX_POS_FORWARD) / 2
    POSITION_ON_BAR_FORWARD_LEFT = (COURT_HEIGHT - MAX_POS_FORWARD + 2 * DISTANCE_FIGURES) / 2
    ABS_X_POSITION = BAR_POSITION_FORWARD
    X_REFLECTION_PLANE = ABS_X_POSITION + FIGURE_FOOT_WIDTH + BALL_RADIUS
    X_OFFSET_REFLECTION_PLANE = FIGURE_FOOT_WIDTH + BALL_RADIUS
    Y_OFFSET_REFLECTION_PLANE = FIGURE_FOOT_HEIGHT / 2 + BALL_RADIUS

    def __init__(self):
        super().__init__(MAX_POS_FORWARD / 2)
        self.intersection_FORWARD = 0
        self.flag_right = False
        self.flag_middle = False
        self.flag_left = False
        self.v_bar = 0
        self.stop_flag = False
    '''hier fehlen noch Methoden fürs Schießen und Collision der Spieler mit Ball'''
    # Phils scheiß geht weiter

    def move_bar(self):
        self.next_position = round(self.next_position)
        self.position = round(self.position)
        if self.next_position != self.position:
            if 0 <= self.next_position <= MAX_POS_FORWARD:
                print(self.v_bar)
                print(self.stop_flag)
                if self.next_position > self.position:
                   if self.stop_flag:
                       self.v_bar = self.v_bar - BAR_ACC * SIMULATION_TIME_STEP
                       new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP - 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP)
                       self.position = new_temp_pos
                       if new_temp_pos > self.next_position:
                           self.position = self.next_position
                           self.next_position = -1
                           self.v_bar = 0
                           self.stop_flag = False

                   else:
                        if self.v_bar < BAR_SPEED:
                            self.v_bar = self.v_bar + BAR_ACC * SIMULATION_TIME_STEP
                            if self.v_bar > BAR_SPEED:
                                self.v_bar = BAR_SPEED
                            new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP + 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP)
                            x_stop = (self.v_bar * self.v_bar) / (2 * BAR_ACC)
                            if (self.next_position - self.position) < x_stop:
                                self.stop_flag = True


                        elif self.v_bar == BAR_SPEED:
                            new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP
                            x_stop = (self.v_bar * self.v_bar) / (2 * BAR_ACC)
                            if (self.next_position - self.position) < x_stop:
                                self.stop_flag = True


                        self.position = new_temp_pos

                elif self.next_position < self.position:
                    if self.stop_flag:
                        self.v_bar = self.v_bar + BAR_ACC * SIMULATION_TIME_STEP
                        new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP + 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP)
                        self.position = new_temp_pos
                        if new_temp_pos < self.next_position:
                            self.position = self.next_position
                            self.next_position = -1
                            self.v_bar = 0
                            self.stop_flag = False

                    else:
                        if self.v_bar >= -BAR_SPEED:
                            self.v_bar = self.v_bar - BAR_ACC * SIMULATION_TIME_STEP
                            if self.v_bar < -BAR_SPEED:
                                self.v_bar = -BAR_SPEED
                            new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP - 0.5 * BAR_ACC * (SIMULATION_TIME_STEP * SIMULATION_TIME_STEP)
                            x_stop = (self.v_bar * self.v_bar) / (2 * BAR_ACC)
                            if (self.position - self.next_position) < x_stop:
                                self.stop_flag = True

                        elif self.v_bar == BAR_SPEED:
                            new_temp_pos = self.position + self.v_bar * SIMULATION_TIME_STEP
                            x_stop = (self.v_bar * self.v_bar) / (2 * BAR_ACC)
                            if (self.position - self.next_position) < x_stop:
                                self.stop_flag = True

                        self.position = new_temp_pos
            else:
                self.next_position = -1
                self.v_bar = 0
        else:
            self.next_position = -1
            self.v_bar = 0


    def reset_bar(self):
        self.next_position = -1
        self.position = MAX_POS_FORWARD / 2
        self.v_bar = 0
        self.stop_flag = False


    def check_for_interaction(self, kicker):
        if kicker.ball.pos[Coordinate.X] > self.X_REFLECTION_PLANE:
            self.check_for_intersection_with_bar(kicker)
            if kicker.ball.pos[Coordinate.X] - self.X_REFLECTION_PLANE <= (kicker.ball.pos[Coordinate.X] -
                                                                           kicker.ball.new_pos[Coordinate.X]):
                shoot = self.check_for_shoot(kicker)
            else:
                shoot = False

            side_collision = False
        elif self.X_REFLECTION_PLANE - kicker.ball.pos[Coordinate.X] < (kicker.ball.speed * SIMULATION_TIME_STEP +
                                                                        self.X_OFFSET_REFLECTION_PLANE):
            side_collision = self.check_for_side_collision(kicker)
            shoot = False
        else:
            side_collision = False
            shoot = False
        return shoot, side_collision


    def check_for_shoot(self, kicker):
        intersection = kicker.ball.pos[Coordinate.Y] - math.tan(kicker.ball.angle) * \
                       (kicker.ball.pos[Coordinate.X] - self.X_REFLECTION_PLANE)
        if self.position + self.POSITION_ON_BAR_FORWARD_RIGHT - self.Y_OFFSET_REFLECTION_PLANE < intersection \
                < self.position + self.POSITION_ON_BAR_FORWARD_RIGHT + self.Y_OFFSET_REFLECTION_PLANE:
            self.shoot(kicker, intersection, TeamHuman.FORWARD_RIGHT)
            shoot = True
        elif self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE - self.Y_OFFSET_REFLECTION_PLANE < intersection \
                < self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE + self.Y_OFFSET_REFLECTION_PLANE:
            self.shoot(kicker, intersection, TeamHuman.FORWARD_CENTER)
            shoot = True
        elif self.position + self.POSITION_ON_BAR_FORWARD_LEFT - self.Y_OFFSET_REFLECTION_PLANE < intersection \
                < self.position + self.POSITION_ON_BAR_FORWARD_LEFT + self.Y_OFFSET_REFLECTION_PLANE:
            self.shoot(kicker, intersection, TeamHuman.FORWARD_LEFT)
            shoot = True
        else:
            shoot = False
        return shoot


    def check_for_side_collision(self, kicker):
        if kicker.ball.angle > 0:
            if kicker.ball.pos[Coordinate.Y] < (self.position + self.POSITION_ON_BAR_FORWARD_LEFT -
                                                self.Y_OFFSET_REFLECTION_PLANE) < kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (self.position + self.POSITION_ON_BAR_FORWARD_LEFT -
                                                                self.Y_OFFSET_REFLECTION_PLANE -
                                                                kicker.ball.pos[Coordinate.Y]) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (self.position + self.POSITION_ON_BAR_FORWARD_LEFT -
                                         self.Y_OFFSET_REFLECTION_PLANE - kicker.ball.pos[Coordinate.Y]) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_LEFT -
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False

            elif kicker.ball.pos[Coordinate.Y] < self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE \
                    - self.Y_OFFSET_REFLECTION_PLANE < kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE -
                                                                self.Y_OFFSET_REFLECTION_PLANE -
                                                                kicker.ball.pos[Coordinate.Y]) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE -
                                         self.Y_OFFSET_REFLECTION_PLANE - kicker.ball.pos[Coordinate.Y]) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE -
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False

            elif kicker.ball.pos[Coordinate.Y] < self.position + self.POSITION_ON_BAR_FORWARD_RIGHT \
                    - self.Y_OFFSET_REFLECTION_PLANE < kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (self.position + self.POSITION_ON_BAR_FORWARD_RIGHT -
                                                                self.Y_OFFSET_REFLECTION_PLANE -
                                                                kicker.ball.pos[Coordinate.Y]) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (self.position + self.POSITION_ON_BAR_FORWARD_RIGHT -
                                         self.Y_OFFSET_REFLECTION_PLANE - kicker.ball.pos[Coordinate.Y]) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_RIGHT -
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False
            else:
                side_collision = False

        elif kicker.ball.angle < 0:
            if kicker.ball.pos[Coordinate.Y] > (self.position + self.POSITION_ON_BAR_FORWARD_RIGHT +
                                                self.Y_OFFSET_REFLECTION_PLANE) > kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (kicker.ball.pos[Coordinate.Y] - self.position -
                                                                self.POSITION_ON_BAR_FORWARD_RIGHT -
                                                                self.Y_OFFSET_REFLECTION_PLANE) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (kicker.ball.pos[Coordinate.Y] - self.position -
                                         self.POSITION_ON_BAR_FORWARD_RIGHT - self.Y_OFFSET_REFLECTION_PLANE) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_RIGHT +
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False

            elif kicker.ball.pos[Coordinate.Y] > (self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE +
                                                  self.Y_OFFSET_REFLECTION_PLANE) > kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (kicker.ball.pos[Coordinate.Y] - self.position -
                                                                self.POSITION_ON_BAR_FORWARD_MIDDLE -
                                                                self.Y_OFFSET_REFLECTION_PLANE) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (kicker.ball.pos[Coordinate.Y] - self.position -
                                         self.POSITION_ON_BAR_FORWARD_MIDDLE - self.Y_OFFSET_REFLECTION_PLANE) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE +
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False

            elif kicker.ball.pos[Coordinate.Y] > (self.position + self.POSITION_ON_BAR_FORWARD_LEFT +
                                                  self.Y_OFFSET_REFLECTION_PLANE) > kicker.ball.new_pos[Coordinate.Y]:
                intersection = kicker.ball.pos[Coordinate.X] + (kicker.ball.pos[Coordinate.Y] - self.position -
                                                                self.POSITION_ON_BAR_FORWARD_LEFT -
                                                                self.Y_OFFSET_REFLECTION_PLANE) / \
                               math.tan(kicker.ball.angle)
                if self.ABS_X_POSITION < intersection < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (kicker.ball.pos[Coordinate.Y] - self.position -
                                         self.POSITION_ON_BAR_FORWARD_LEFT - self.Y_OFFSET_REFLECTION_PLANE) / \
                                        (math.sin(kicker.ball.angle) * kicker.ball.speed)
                    kicker.ball.new_angle = - kicker.ball.angle
                    kicker.ball.new_pos[Coordinate.X] = (kicker.ball.pos[Coordinate.X] + math.cos(kicker.ball.angle) *
                                                         kicker.ball.speed * SIMULATION_TIME_STEP)
                    kicker.ball.new_pos[Coordinate.Y] = (self.position + self.POSITION_ON_BAR_FORWARD_LEFT +
                                                         self.Y_OFFSET_REFLECTION_PLANE +
                                                         math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                                         (SIMULATION_TIME_STEP - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False
            else:
                side_collision = False
        else:
            side_collision = False

        return side_collision


    def shoot(self, kicker, intersection, teammate):
        delta_t_collision = (kicker.ball.pos[Coordinate.X] - self.X_REFLECTION_PLANE) / \
                            (math.cos(kicker.ball.angle) * kicker.ball.speed)
        if teammate == TeamHuman.FORWARD_RIGHT:
            shoot_offset = self.position + self.POSITION_ON_BAR_FORWARD_RIGHT - intersection
        elif teammate == TeamHuman.FORWARD_CENTER:
            shoot_offset = self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE - intersection
        elif teammate == TeamHuman.FORWARD_LEFT:
            shoot_offset = self.position + self.POSITION_ON_BAR_FORWARD_LEFT - intersection
        else:
            raise ValueError('Uebergabeparameter (teammate) in model.HumanDefender.py falsch (Fkt. shoot())')
        kicker.ball.new_angle = ((math.pi / 3) * (- shoot_offset / (FIGURE_FOOT_HEIGHT / 2 + BALL_RADIUS)))
        kicker.ball.speed = SHOOT_SPEED
        kicker.ball.new_pos[Coordinate.Y] = (intersection + math.sin(kicker.ball.new_angle) * kicker.ball.speed *
                                             (SIMULATION_TIME_STEP - delta_t_collision))
        kicker.ball.new_pos[Coordinate.X] = (self.X_REFLECTION_PLANE + math.cos(kicker.ball.new_angle) *
                                             kicker.ball.speed * (SIMULATION_TIME_STEP - delta_t_collision))



    def check_for_intersection_with_bar(self, kicker):
        if kicker.ball.pos[Coordinate.X] > self.X_REFLECTION_PLANE:
            if (kicker.ball.pos[Coordinate.X] - kicker.ball.new_pos[Coordinate.X]) >= 0:
                abstand_quer = -1*((kicker.ball.pos[Coordinate.X] - self.X_REFLECTION_PLANE) / math.cos(kicker.ball.angle))
                abstand_vertikal = math.sin(kicker.ball.angle) * abstand_quer
                delta_t = abstand_quer / kicker.ball.speed
                self.intersection_FORWARD = kicker.ball.pos[Coordinate.Y] + abstand_vertikal
                if 0 < self.intersection_FORWARD <= COURT_HEIGHT:
                    if 0 < self.intersection_FORWARD <= (40 + MAX_POS_FORWARD):
                        #if ((abs(self.POSITION_ON_BAR_FORWARD_RIGHT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                            self.flag_right = True

                    if MAX_POS_FORWARD < self.intersection_FORWARD <= (40 + MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES):
                        #if ((abs(self.POSITION_ON_BAR_FORWARD_MIDDLE - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                            self.flag_middle = True
                    if (MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES) < self.intersection_FORWARD <= COURT_HEIGHT:
                        #if (abs(self.POSITION_ON_BAR_FORWARD_LEFT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t:
                            self.flag_left = True
                else:
                    if self.intersection_FORWARD < 0:
                        self.intersection_FORWARD = -1 * self.intersection_FORWARD
                        if 40 < self.intersection_FORWARD <= (40 + MAX_POS_FORWARD):
                            #if ((abs(self.POSITION_ON_BAR_FORWARD_RIGHT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                                self.flag_right = True
                        if MAX_POS_FORWARD < self.intersection_FORWARD <= (
                                40 + MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES):
                            #if ((abs(self.POSITION_ON_BAR_FORWARD_MIDDLE - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                                self.flag_middle = True
                        if (MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES) < self.intersection_FORWARD <= (
                                40 + MAX_POS_FORWARD + 2 * FORWARD_DISTANCE_BETWEEN_FIGURES):
                            #if (abs(self.POSITION_ON_BAR_FORWARD_LEFT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t:
                                self.flag_left = True
                    elif self.intersection_FORWARD > COURT_HEIGHT:
                        Differenz = self.intersection_FORWARD - COURT_HEIGHT
                        self.intersection_FORWARD = COURT_HEIGHT - Differenz
                        if 40 < self.intersection_FORWARD <= (40 + MAX_POS_FORWARD):
                            #if ((abs(self.POSITION_ON_BAR_FORWARD_RIGHT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                                self.flag_right = True
                        if MAX_POS_FORWARD < self.intersection_FORWARD <= (
                                40 + MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES):
                            #if ((abs(self.POSITION_ON_BAR_FORWARD_MIDDLE - self.intersection_FORWARD) / BAR_SPEED) <= delta_t):
                                self.flag_middle = True
                        if (MAX_POS_FORWARD + FORWARD_DISTANCE_BETWEEN_FIGURES) < self.intersection_FORWARD <= (
                                COURT_HEIGHT):
                            #if (abs(self.POSITION_ON_BAR_FORWARD_LEFT - self.intersection_FORWARD) / BAR_SPEED) <= delta_t:
                                self.flag_left = True
                if self.flag_right and self.flag_middle:
                    self.flag_right = False
                    self.flag_middle = False
                    distance_right = abs(self.intersection_FORWARD - self.position + self.POSITION_ON_BAR_FORWARD_RIGHT)
                    distance_middle = abs(self.intersection_FORWARD - self.position +self.POSITION_ON_BAR_FORWARD_MIDDLE)
                    if distance_right < distance_middle:
                        self.flag_right = True
                    elif distance_middle <= distance_right:
                        self.flag_middle = True

                elif self.flag_middle and self.flag_left:
                    self.flag_middle = False
                    self.flag_left = False
                    distance_middle = abs(self.intersection_FORWARD - self.position + self.POSITION_ON_BAR_FORWARD_MIDDLE)
                    distance_left = abs(self.intersection_FORWARD - self.position + self.POSITION_ON_BAR_FORWARD_LEFT)
                    if distance_middle <= distance_left:
                        self.flag_middle = True
                    elif distance_middle < distance_left:
                        self.flag_left = True