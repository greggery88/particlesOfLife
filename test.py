import unittest
import particle
import logging
import pygame
from pygame.math import *

log = logging.getLogger("particlesOfLife")


class ParticleForceCalc(unittest.TestCase):
    def test_force_direction_2_pt(self):
        # defining particles
        nc = 1
        matrix = [[1]]
        p1 = particle.Particle(nc, 0, 0, matrix)
        p2 = particle.Particle(nc, -3, 0, matrix)
        # defining need variables
        ceof = 1
        pts = [p1, p2]
        r = 15

        # updating particles
        p1_resulting_force = p1.resulting_calculated_forces(
            p1.find_nearby_particles(pts, r), ceof
        )
        p2_resulting_force = p2.resulting_calculated_forces(
            p2.find_nearby_particles(pts, r), ceof
        )

        print(str(p1_resulting_force) + "" + " <- p1")
        print(str(p2_resulting_force) + "" + " <- p2")
        print(str(p1_resulting_force.normalize()) + "" + " <- p1_norm")
        print(str(p2_resulting_force.normalize()) + "" + " <- p2_norm")
        self.assertEqual(round(p1_resulting_force.magnitude()), 5)
        self.assertEqual(round(p2_resulting_force.magnitude()), 5)
        self.assertEqual(p1_resulting_force, Vector2(-4.87095, 0))
        self.assertEqual(p2_resulting_force, Vector2(4.87095, 0))

    def test_force_direction_3_pt(self):
        # defining particles
        nc = 1
        matrix = [[1]]
        p1 = particle.Particle(nc, -2.886, 0, matrix)
        p2 = particle.Particle(nc, 0, 0, matrix)
        p3 = particle.Particle(nc, 4.0, 0, matrix)
        # defining need variables
        ceof = 1
        pts = [p1, p2, p3]
        r = 15

        # updating particles
        p1_resulting_force = p1.resulting_calculated_forces(
            p1.find_nearby_particles(pts, r), ceof
        )
        p2_resulting_force = p2.resulting_calculated_forces(
            p2.find_nearby_particles(pts, r), ceof
        )
        p3_resulting_force = p3.resulting_calculated_forces(
            p3.find_nearby_particles(pts, r), ceof
        )
        print(str(p1_resulting_force) + "" + " <- p1_")
        print(str(p2_resulting_force) + "" + " <- p2_")
        print(str(p3_resulting_force) + "" + " <- p3_")
        self.assertEqual(round(p1_resulting_force.magnitude()), 5)
        self.assertEqual(round(p2_resulting_force.magnitude()), 4)
        self.assertEqual(round(p3_resulting_force.magnitude()), 1)

    def test_force_calculation_in_range(self):
        x = -30
        y = 61

        p = particle
        v = pygame.Vector2(x, y)

        r = 2.886
        fc = p._force_calculator(v, 1, r)
        print(fc.magnitude())
        self.assertEqual(round(fc.magnitude()), 5)
        r = 4.0
        fc = p._force_calculator(v, 1, r)
        print(fc.magnitude())
        self.assertEqual(round(fc.magnitude()), 1)
        r = 3.326
        fc = p._force_calculator(v, 1, r)
        print(fc.magnitude())
        self.assertEqual(round(fc.magnitude()), 3)

    def test_find_particles_func(self):
        r = 20

        # defines the particles and makes a list

        p1 = particle.Particle(1, 0, 0, [[1]])
        p2 = particle.Particle(1, 1, 0, [[1]])
        p3 = particle.Particle(1, 0, 1, [[1]])
        p4 = particle.Particle(1, 5, 5, [[1]])
        p5 = particle.Particle(1, 16, 12, [[1]])
        p6 = particle.Particle(1, 15, 15, [[1]])
        p7 = particle.Particle(1, 21, 0, [[1]])
        p8 = particle.Particle(1, 0, 21, [[1]])
        pt_list = [p1, p2, p3, p4, p5, p6, p7, p8]

        self.assertListEqual(p1.find_nearby_particles(pt_list, r), [p2, p3, p4])
        self.assertNotEqual(p1.find_nearby_particles(pt_list, r), [p5, p6, p7, p8])

    def test_calc_resulting_force(self):

        # add particles and list of particles

        p1 = particle.Particle(1, 0, 0, [[-1]])

        self.assertEqual(p1.resulting_calculated_forces([], 1).x, 0)
        self.assertEqual(p1.resulting_calculated_forces([], 1).y, 0)

        p2 = particle.Particle(1, 0, 1, [[-1]])

        result = p1.resulting_calculated_forces([p2], 1)

        self.assertAlmostEqual(result.x, 0)
        self.assertAlmostEqual(result.y, -30.585, 3)

        p2 = particle.Particle(1, 0, 2.886, [[-1]])

        result = p1.resulting_calculated_forces([p2], 1)

        self.assertAlmostEqual(result.x, 0, 1)
        self.assertAlmostEqual(result.y, -5, 1)

        p2 = particle.Particle(1, 0, 2.886, [[-1]])
        p3 = particle.Particle(1, 2.886, 0, [[-1]])
        result = p1.resulting_calculated_forces([p2, p3], 1)

        self.assertAlmostEqual(result.x, -5, 0)
        self.assertAlmostEqual(result.y, -5, 0)


if __name__ == "__main__":
    unittest.main()
