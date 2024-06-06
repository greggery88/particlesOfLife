import pygame as pyg
import random as rd
from pygame import Vector2

# particle Global
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


class Particle:
    def __init__(self, number_of_colors, x, y, matrix):
        # initializing the position, velocity, mass
        self.velocity = Vector2(0, 0)
        self.position = Vector2(x, y)
        self.radius = 1
        self.half_life = 10
        self.applied_force = Vector2(0, 0)
        # color
        self.color = _color(number_of_colors)
        self.cn = number_of_colors
        self.matrix = matrix

    def update(self, coefficient_of_force, particles, radius):
        self.applied_force = self.resulting_calculated_forces(
            self.find_nearby_particles(particles, radius), coefficient_of_force
        )
        self.velocity = self.applied_force  # + self.velocity
        self.position = self.position + self.velocity
        if (
            self.velocity != 0
            and abs(
                self.velocity.magnitude()
                - ((3 * self.velocity) / (2 * self.half_life)).magnitude()
            )
            < self.velocity.magnitude()
        ):
            # self.velocity = self.velocity - (3 * self.velocity) / (2 * self.half_life)
            pass

    def draw(self, scr):
        pyg.draw.circle(
            scr,
            self.color,
            self.position,
            self.radius,
        )

    def find_nearby_particles(self, particles, thresh_hold_radius):
        nearby_pt = []
        to_close_pt = []
        in_radius_pt = []
        for particle in particles:
            distance = (
                # Vector2.__sub__(particle.position, self.position)
                particle.position
                - self.position
            ).magnitude()
            if distance < self.radius + 2 and distance != 0:
                to_close_pt.append(particle)
            elif (
                distance < self.radius + 10
                and distance != 0
                and self.color != particle.color
            ):
                to_close_pt.append(particle)
            elif distance < thresh_hold_radius and distance != 0:
                in_radius_pt.append(particle)
            elif distance == 0 and particle != self:
                to_close_pt.append(particle)
        nearby_pt.append(to_close_pt)
        nearby_pt.append(in_radius_pt)
        return nearby_pt

    def _scaler_matrix(self, nc, ptc):
        scaler = float
        matrix = self.matrix
        if self.color == red:
            row = matrix[0]
            if ptc == red:
                scaler = row[0]
            if ptc == blue:
                scaler = row[1]
            if ptc == green:
                scaler = row[2]
        if self.color == blue:
            row = matrix[1]
            if ptc == red:
                scaler = row[0]
            if ptc == blue:
                scaler = row[1]
            if ptc == green:
                scaler = row[2]
        if self.color == green:
            row = matrix[2]
            if ptc == red:
                scaler = row[0]
            if ptc == blue:
                scaler = row[1]
            if ptc == green:
                scaler = row[2]
        return scaler

    def resulting_calculated_forces(self, nearby_pt, coefficient_force):
        resulting_force_list = []
        resulting_force = pyg.math.Vector2(0, 0)
        if len(nearby_pt[0]) == 0 and len(nearby_pt[1]) == 0:
            resulting_force_list.append(pyg.Vector2(0, 0))
        else:
            # for to_close particles
            for particle in nearby_pt[0]:
                vec_self_to_pt = particle.position + self.position

                resulting_force_list.append(
                    (
                        _force_calculator(
                            vec_self_to_pt,
                            0.01 * coefficient_force,
                            pyg.math.Vector2.magnitude(particle.position),
                        )
                    )
                )

            # for particles in radius
            for particle in nearby_pt[1]:
                scaler = self._scaler_matrix(self.cn, particle.color)
                vec_self_to_pt = particle.position - self.position
                resulting_force_list.append(
                    (
                        scaler
                        * (
                            _force_calculator(
                                vec_self_to_pt,
                                coefficient_force,
                                pyg.math.Vector2.magnitude(particle.position),
                            )
                        )
                    )
                )
        for Vector2 in resulting_force_list:
            resulting_force = resulting_force + Vector2
            return resulting_force


def _force_calculator(vector, coefficient, radius):
    force = (coefficient * vector) / radius**2
    return force


def _color(number):
    if number < 1:
        number = 1
    # colors
    color = (int, int, int)
    color_number = rd.randint(1, number)
    if color_number == 1:
        color = red
    elif color_number == 2:
        color = blue
    elif color_number == 3:
        color = green
    return color
