#!/usr/bin/env python3
"""
Minecraft railroad with setblock commands in vanilla minecraft

E.g. usage:
./dome -x 82 -z 358 -y 63 -l 40
Capture the output and paste it into the console
"""


import argparse


def main():
    parser = argparse.ArgumentParser(description="create commands for " +
                                        "railroad")
    parser.add_argument("-x", "--x-center", type=int, required=True,
                        help="center of structure in x dimension")
    parser.add_argument("-z", "--z-center", type=int, required=True,
                        help="center of structure in z dimension")
    parser.add_argument("-y", "--y-level", type=int, required=True,
                        help="bottom of structure in y dimension")
    parser.add_argument("-d", "--dir", type=int, required=True,
                        help="direction to extend tracks (+-1=x, +-3=z)")
    parser.add_argument("-l", "--track-sections", type=int, 
                        required=True,
                        help="the length of the track in sections")

    args = parser.parse_args()

    track_sections = args.track_sections
    x_center = args.x_center
    y_level = args.y_level
    z_center = args.z_center
    dir = args.dir
    track_length = 4

    if dir == -1:
        x_dir = -1
        z_dir = 0
    elif dir == 1:
        x_dir = 1
        z_dir = 0
    elif dir == -3:
        x_dir = 0
        z_dir = -1
    elif dir == 3:
        x_dir = 0
        z_dir = 1
    else:
        raise Exception("invalid direction value")

    for i in range(track_sections):
        x_offset = i * track_length * x_dir
        z_offset = i * track_length * z_dir
        for j in range(track_length):
            if x_dir != 0:
                x_j = j
                z_j = 0
                x_w = 0 
                z_w = 1 
            elif z_dir != 0:
                x_j = 0
                z_j = j
                x_w = 1
                z_w = 0
            if j == 0:
                print("/setblock {0} {1} {2} {3}".format(
                    x_center + x_offset + x_j, 
                    y_level, z_center + z_offset + z_j, 
                    "minecraft:concrete 15"))
                print("/setblock {0} {1} {2} {3}".format(
                    x_center + x_offset + x_j, 
                    y_level + 1, z_center + z_offset + z_j,
                    "minecraft:redstone_torch 5"))
            else:
                print("/setblock {0} {1} {2} {3}".format(
                    x_center + x_offset + x_j, 
                    y_level, z_center + z_offset + z_j, 
                    "minecraft:gold_block"))
            for k in range(-3, 4, 1):
                if k == 0 and j == 0:
                    continue
                print("/setblock {0} {1} {2} {3}".format(
                    x_center + x_offset + x_j + x_w * k,
                    y_level, z_center + z_offset + z_j + z_w * k,
                    "minecraft:concrete 15"))
                if k == 1 or k == -1:
                    print("/setblock {0} {1} {2} {3}".format(
                        x_center + x_offset + x_j + x_w * k, 
                        y_level + 1, z_center + z_offset + z_j + z_w * k,
                        "minecraft:golden_rail"))



if __name__ == "__main__":
        main()
