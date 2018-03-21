#!/usr/bin/env python3
"""
Minecraft dome with setblock commands in vanilla minecraft

E.g. usage:
./dome -x 82 -z 358 -y 63 -r 40
Capture the output and paste it into the console
"""


import argparse
import math


def distance(x, z, y):
    """
    Three dimensional distance function.
    """

    return math.sqrt(math.pow(x, 2) + math.pow(z, 2) + math.pow(y, 2))


def main():
    parser = argparse.ArgumentParser(description="create commands for " +
                                        "modular tiered fortress")
    parser.add_argument("-x", "--x-center", type=int, required=True,
                        help="center of structure in x dimension")
    parser.add_argument("-z", "--z-center", type=int, required=True,
                        help="center of structure in z dimension")
    parser.add_argument("-y", "--y-bottom", type=int, required=True,
                        help="bottom of structure in y dimension")
    parser.add_argument("-r", "--dome_radius", type=int, required=True,
                        help="the radius of the dome")

    args = parser.parse_args()

    radius = args.dome_radius
    x_center = args.x_center
    y_bottom = args.y_bottom
    z_center = args.z_center
    for x in range(radius * -1, radius):
        for z in range(radius * -1, radius):
            for y in range(0, radius):
                if distance(x, z, y) < radius and distance(x, z, y) > radius-3:
                    print("/setblock {0} {1} {2} {3}".format(
                          x+x_center, y + y_bottom, z+z_center, "minecraft:glass"))

    radius -= 3
    for x in range(radius * -1, radius):
        for z in range(radius * -1, radius):
            for y in range(0, radius):
                if distance(x, z, y) < radius:
                    print("/setblock {0} {1} {2} {3}".format(
                        x+x_center, y_bottom, z+z_center, "minecraft:air"))



if __name__ == "__main__":
        main()
