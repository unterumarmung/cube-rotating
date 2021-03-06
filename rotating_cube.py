import numpy
from quat import Quaternion

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from utils import OpenGLContext


class RotatingCube:
    def __init__(self):
        window_size = self.init_pygame()
        self.init_opengl(window_size)

    def update(self, quat: Quaternion):
        self.update_opengl(quat.get_mat4())
        self.draw_cube()
        self.draw_axis()
        self.update_pygame()

    axis_verts = (
        (-7.5, 0.0, 0.0),
        (7.5, 0.0, 0.0),
        (0.0, -7.5, 0.0),
        (0.0, 7.5, 0.0),
        (0.0, 0.0, -7.5),
        (0.0, 0.0, 7.5)
    )

    axes = (
        (0, 1),
        (2, 3),
        (4, 5)
    )

    axis_colors = (
        (1.0, 0.0, 0.0),  # Red
        (0.0, 1.0, 0.0),  # Green
        (0.0, 0.0, 1.0)  # Blue
    )

    '''
       5____________6
       /           /|
      /           / |
    1/__________2/  |
    |           |   |
    |           |   |
    |           |   7
    |           |  /
    |           | /
    0___________3/
    '''

    cube_verts = (
        (-3.0, -3.0, 3.0),
        (-3.0, 3.0, 3.0),
        (3.0, 3.0, 3.0),
        (3.0, -3.0, 3.0),
        (-3.0, -3.0, -3.0),
        (-3.0, 3.0, -3.0),
        (3.0, 3.0, -3.0),
        (3.0, -3.0, -3.0)
    )

    cube_edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 6),
        (5, 1),
        (5, 4),
        (5, 6),
        (7, 3),
        (7, 4),
        (7, 6)
    )

    cube_surfaces = (
        (0, 1, 2, 3),  # Front
        (3, 2, 6, 7),  # Right
        (7, 6, 5, 4),  # Left
        (4, 5, 1, 0),  # Back
        (1, 5, 6, 2),  # Top
        (4, 0, 3, 7)  # Bottom
    )

    cube_colors = (
        (0.769, 0.118, 0.227),  # Red
        (0.0, 0.318, 0.729),  # Blue
        (1.0, 0.345,  0.0),  # Orange
        (0.0, 0.62, 0.376),  # Green
        (1.0,  1.0,  1.0),  # White
        (1.0, 0.835,  0.0)  # Yellow
    )

    def draw_axis(self):
        with OpenGLContext(GL_LINES) as context:
            for color, axis in zip(self.axis_colors, self.axes):
                glColor3fv(color)
                for point in axis:
                    glVertex3fv(self.axis_verts[point])

    def draw_cube(self):
        with OpenGLContext(GL_QUADS) as context:
            for color, surface in zip(self.cube_colors, self.cube_surfaces):
                glColor3fv(color)
                for vertex in surface:
                    glVertex3fv(self.cube_verts[vertex])

        with OpenGLContext(GL_LINES) as context:
            glColor3fv((0.0, 0.0, 0.0))
            for edge in self.cube_edges:
                for vertex in edge:
                    glVertex3fv(self.cube_verts[vertex])

    def init_pygame(self):
        # Try to center the window
        import os
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Init the window
        pygame.init()
        screen = pygame.display.set_mode()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        display = (width/2, height/2)
        pygame.display.set_mode((width/2, height/2), DOUBLEBUF | OPENGL)

        return display

    def init_opengl(self, window_size):
        # Using depth test to make sure closer colors are shown over further ones
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # Default view
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (window_size[0]/window_size[1]), 0.5, 40)
        glTranslatef(0.0, 0.0, -17.5)

    def update_opengl(self, mat4):
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(mat4)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update_pygame(self):
        pygame.display.flip()
        pygame.time.wait(10)
