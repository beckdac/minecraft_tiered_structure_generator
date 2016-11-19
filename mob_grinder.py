#!/usr/bin/env python3
"""
Minecraft mob spawner generator
with setblock commands in vanilla minecraft

E.g. usage:
./mob_grinder.py -x 82 -z 358 -y 60 -b minecraft:cobblestone 
Capture the output and paste it into the console
"""


import argparse
import math


def set_block(x, y, z, block_id):
    """
    Set a block of a specified type
    """

    print("/setblock {0} {1} {2} {3}".format(
        x, y, z, block_id))


def fall_trap_level(x_center, y, z_center, block_id):
    x = x_center
    y_current = y
    z = z_center
    set_block(x - 1, y, z, block_id)
    set_block(x - 1, y, z + 1, block_id)
    set_block(x, y, z + 2, block_id)
    set_block(x + 1, y, z + 2, block_id)
    set_block(x + 2, y, z + 1, block_id)
    set_block(x + 2, y, z, block_id)
    set_block(x + 1, y, z - 1, block_id)
    set_block(x, y, z - 1, block_id)
    set_block(x, y, z, "minecraft:air")
    set_block(x + 1, y, z, "minecraft:air")
    set_block(x, y, z + 1, "minecraft:air")
    set_block(x + 1, y, z + 1, "minecraft:air")


def mob_spawner(x_center, y_bottom, z_center, block_id):
    """
    Generate a mob spawner with a specified block id.


    Keyword arguments:
    x_center -- the center of the structure in the x dimension
    y_bottom -- the base of the structure in the y dimension
    z_center -- the center of the structure in the z dimension
    block_id -- the block type for the hard parts of the structure
    """

    chamber_height = 28
    # increment y_bottom to leave room for chests
    y_current = y_bottom + 1
    # hoppers
    for x in range(2):
        for z in range(2):
            set_block(x + x_center, y_current, z + z_center,
             "minecraft:hopper")
    y_current += 1
    # fall chute
    x = x_center
    z = z_center
    for y in range(1, 3):
        fall_trap_level(x_center, y + y_bottom + 1, z_center, "minecraft:glass")
    for y in range(3, chamber_height):
        fall_trap_level(x_center, y + y_bottom + 1, z_center, block_id)
    # spawning chamber
    y_current = y_bottom + 1 + chamber_height
    # floor
    for x in range(-9, 11):
        for z in range(-9, 11):
            set_block(x + x_center, y_current + 1, z + z_center, block_id);
    # channel walls
    for x in [-1, 2]:
        for z in range(-9, 11):
            set_block(x + x_center, y_current, z + z_center, block_id);
    for x in range(-9, 11):
        for z in [-1, 2]:
            set_block(x + x_center, y_current, z + z_center, block_id);
    # water channels
    for x in range(2):
        for z in range(-9, 11):
            set_block(x + x_center, y_current + 1, z + z_center, "minecraft:air");
            set_block(x + x_center, y_current, z + z_center, "minecraft:air");
            set_block(x + x_center, y_current - 1, z + z_center, block_id);
    for x in range(-9, 11):
        for z in range(2):
            set_block(x + x_center, y_current + 1, z + z_center, "minecraft:air");
            set_block(x + x_center, y_current, z + z_center, "minecraft:air");
            set_block(x + x_center, y_current - 1, z + z_center, block_id);
    # water channel end cap
    for x in range(2):
        for z in [-9, 10]:
            for y in range(2):
                set_block(x + x_center, y_current + y, z + z_center, block_id);
    for z in range(2):
        for x in [-9, 10]:
            for y in range(2):
                set_block(x + x_center, y_current + y, z + z_center, block_id);
    # water in the channel
    for x in range(2):
        for z in [-8, 9]:
            set_block(x + x_center, y_current, z + z_center, "minecraft:flowing_water")
    for z in range(2):
        for x in [-8, 9]:
            set_block(x + x_center, y_current, z + z_center, "minecraft:flowing_water")
    # floor chute hole
    for x in range(2):
        for z in range(2):
            set_block(x + x_center, y_current - 1, z + z_center, "minecraft:air");
    # floor walls
    for x in [-9, 10]:
        for z in range(-9, 11):
            for y in range(1,3):
                set_block(x + x_center, y_current + y + 1, z + z_center, block_id);
    for z in range(-9, 11):
        for x in [-9, 10]:
            for y in range(1,3):
                set_block(x + x_center, y_current + y + 1, z + z_center, block_id);
    for z in [-9, 10]:
        for x in range(-9, 11):
            for y in range(1,3):
                set_block(x + x_center, y_current + y + 1, z + z_center, block_id);
    for x in range(-9, 11):
        for z in [-9, 10]:
            for y in range(1,3):
                set_block(x + x_center, y_current + y + 1, z + z_center, block_id);
    # roof
    for x in range(-8, 10):
        for z in range(-8, 10):
            set_block(x + x_center, y_current + 4, z + z_center, block_id);
    



def main():
    parser = argparse.ArgumentParser(description="create commands for " +
                                        "mob spawner")
    parser.add_argument("-x", "--x-center", type=int, required=True,
                        help="center of structure in x dimension")
    parser.add_argument("-z", "--z-center", type=int, required=True,
                        help="center of structure in z dimension")
    parser.add_argument("-y", "--y-bottom", type=int, required=True,
                        help="bottom of structure in y dimension")
    parser.add_argument("-b", "--block_id", type=str, required=True,
                        help="the block id of the hard block")

    args = parser.parse_args()

    mob_spawner(args.x_center, args.y_bottom, args.z_center, 
                        args.block_id)


if __name__ == "__main__":
        main()
