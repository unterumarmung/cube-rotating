from rotating_cube import RotatingCube
from quat import Quaternion
from time import sleep


def main():
    cube = RotatingCube()

    with open('simple_example.txt') as file:
        for line in file:
            line = line.strip()
            if line == '':
                continue
            sleep(0.5)
            rotation = Quaternion.from_string(line)
            cube.update(rotation)


if __name__ == '__main__':
    main()
