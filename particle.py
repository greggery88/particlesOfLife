import pygame as pyg
import random as rd
from pygame import Vector2


# particle Global
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


class Particle:

    def __init__(self, number_of_colors, x, y, matrix):

        # initializing the particles properties and self values

        # movement and position properties

        self.velocity = Vector2(0, 0)
        self.position = Vector2(x, y)
        self.applied_force = Vector2(0, 0)

        # view properties

        self.radius = 2
        self.color = _color(number_of_colors)
        self.cn = number_of_colors

        # advanced movement properties
        self.r_min = 6
        self.r_max = 30
        self.half_life = 10
        self.matrix = matrix

    def update_velocity(self, coefficient_of_force, particles, radius):

        # lowers velocity with half lfe

        self.velocity -= self.velocity / 1.01

        # find the force applied to the particle

        self.applied_force = self.resulting_calculated_forces(
            self.find_nearby_particles(particles, radius), coefficient_of_force
        )

        # works out the new velocity from the applied force

        self.velocity = self.applied_force + self.velocity

    def update_position(self):

        # Updates the particle's position

        self.position = self.position + self.velocity

    def draw(self, scr):

        # draws the particle

        pyg.draw.circle(
            scr,
            self.color,
            self.position,
            self.radius,
        )

    def find_nearby_particles(self, particles, thresh_hold_radius):

        # creates the list of nearby particles

        nearby_pt = []

        # adds particles to the list if within distance

        for particle in particles:

            distance = self.position.distance_to(particle.position)

            if distance < thresh_hold_radius and particle != self:
                nearby_pt.append(particle)

        return nearby_pt

    def _scaler_matrix(self, ptc):
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

    def resulting_calculated_forces(self, nearby_pt, coefficient):

        # creates  a list to store the force from each particle.

        resulting_force_list = []
        resulting_force = Vector2(0, 0)

        # check if there are any nearby particles.

        if len(nearby_pt) == 0:
            resulting_force_list.append(Vector2(0, 0))

        else:

            # loop for all nearby particles to find there in fluence then appending them on to a list.

            for particle in nearby_pt:

                # calcu displacement.
                vector = particle.position - self.position
                r = vector.magnitude()

                # calc force
                scaler = self._scaler_matrix(particle.color)
                force = self._force_calculator(vector, coefficient, r, scaler)

                resulting_force_list.append(force)

        for pyg.Vector2 in resulting_force_list:
            resulting_force = resulting_force + pyg.Vector2
        return resulting_force

    def _force_calculator(self, vector, coefficient, radius, scaler):
        # important scaler for the force calculation
        r_min = self.r_min
        r_max = self.r_max
        r_mid = (r_max + r_min) / 2
        const_a = 1 / r_min
        const_b = 1 / (r_mid - r_min)

        # check if the particle is in another particle if so return a random low force.

        if radius == 0:
            force = Vector2(rd.uniform(-0.001, 0.001), rd.uniform(-0.001, 0.001))
            return force

        # defines radius scaler and sets its value.

        rs = float
        if radius < r_min:
            rs = const_a * radius - 1

        elif r_min <= radius < r_mid:
            rs = scaler * const_b * (radius - r_min)

        elif r_mid < radius <= r_max:
            rs = -scaler * const_b * (radius - r_max)

        # calculates and returns force for non 0 vectors

        force = rs * coefficient * vector.normalize()
        return force


def _color(number):

    # defines what a color is.

    color = (int, int, int)

    # randomize the color of the particles

    color_number = rd.randint(1, number)

    # sets the color

    if color_number == 1:
        color = red
    elif color_number == 2:
        color = blue
    elif color_number == 3:
        color = green
    return color
