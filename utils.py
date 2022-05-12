from OpenGL.GL import *


class OpenGLContext(object):
    def __init__(self, init_value):
        self.init_value = init_value

    def __enter__(self):
        glBegin(self.init_value)
        return self

    def __exit__(self, type, value, traceback):
        glEnd()
