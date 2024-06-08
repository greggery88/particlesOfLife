import pygame as pyg
import particle as ptc
import random as rd
import logging

coefficient_of_force = 100
radius_for_force = 30
number_of_colors = 3
number_particles = 1000

log = logging.getLogger(__name__)


def make_matrix(nc):
    matrix = []
    # for _ in range(nc):
    # matrix.append([rd.uniform(1, -1) for _ in range(nc)])
    # print(matrix)
    matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    return matrix


def main():
    logging.basicConfig(level=logging.INFO)
    clock = pyg.time.Clock()
    matrix = []
    matrix = make_matrix(number_of_colors)

    particles = [
        ptc.Particle(number_of_colors, rd.uniform(0, 500), rd.uniform(0, 500), matrix)
        for _ in range(number_particles)
    ]

    # Main loop
    running = True
    while running:

        # quit function
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                quit()

        pyg.Surface.fill(screen, (0, 0, 0))
        for particle in particles:
            particle.update_velocity(coefficient_of_force, particles, radius_for_force)
        for particle in particles:
            particle.update_position()
        for particle in particles:
            particle.draw(screen)
        clock.tick(60)
        pyg.display.update()
        fps = clock.get_fps()
        pyg.display.set_caption("fps = " + "" + str(fps))


if __name__ == "__main__":
    pyg.init()
    screen = pyg.display.set_mode((500, 500))
    main()
