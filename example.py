import pygame
from math import pi
from quat import Quaternion
from rotating_cube import RotatingCube


def main():
    cube = RotatingCube()

    inc_x = 0
    inc_y = 0
    accum = Quaternion.from_value((1, 0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                # Rotating about the x axis
                if event.key == pygame.K_UP:
                    inc_x = pi/100
                if event.key == pygame.K_DOWN:
                    inc_x = -pi/100

                # Rotating about the y axis
                if event.key == pygame.K_LEFT:
                    inc_y = pi/100
                if event.key == pygame.K_RIGHT:
                    inc_y = -pi/100

                # Reset to default view
                if event.key == pygame.K_SPACE:
                    accum = Quaternion.from_value((1, 0, 0, 0))

            if event.type == pygame.KEYUP:
                # Stoping rotation
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    inc_x = 0.0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    inc_y = 0.0

        rot_x = Quaternion.from_axisangle(inc_x, (1.0, 0.0, 0.0))
        rot_y = Quaternion.from_axisangle(inc_y, (0.0, 1.0, 0.0))
        accum = accum * rot_x
        accum = accum * rot_y

        cube.update(accum)


main()
