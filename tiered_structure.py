#!/usr/bin/env python3
"""
Minecraft tiered structure generator
with setblock commands in vanilla minecraft

E.g. usage:
./tiered_structure.py -x 82 -z 358 -y 63 -t 4 -w 10 -b minecraft:cobblestone -f minecraft:fence -e 4
Capture the output and paste it into the console
"""


import argparse
import math


def distance(x, z):
    """
    Two dimensional distance function.
    """

    return math.sqrt(math.pow(x, 2) + math.pow(z, 2))


def filled(x, z, radius):
    """
    Boolean function if a block should be filled
    """

    return distance(x, z) <= radius


def fat_filled(x, z, radius):
    """
    Boolean function for fat wall filling"
    """

    return filled(x, z, radius) and not (
            filled(x + 1, z, radius) and
            filled(x - 1, z, radius) and
            filled(x, z + 1, radius) and
            filled(x, z - 1, radius) and
            filled(x + 1, z + 1, radius) and
            filled(x + 1, z - 1, radius) and
            filled(x - 1, z - 1, radius) and
            filled(x - 1, z + 1, radius));


def circle_setblock(radius, x_center, y, z_center, block_id, thin=False,
                        set_facing = False):
    """
    Draw a circle of radius at y height with block_id type.
    """

    for x in range(radius*-1, radius):
        for z in range(radius*-1, radius):
            if not thin:
                is_filled = fat_filled(x, z, radius)
            else:
                if x > 0:
                    x_trim = 1
                else:
                    x_trim = -1
                if z > 0:
                    z_trim = 1
                else:
                    z_trim = -1
                is_filled = fat_filled(x, z, radius) and not (
                    fat_filled(x+x_trim, y, radius) and
                    fat_filled(x, z+z_trim, radius))
                        
            if is_filled:
                if not set_facing:
                    print("/setblock {0} {1} {2} {3}".format(
                        x+x_center, y, z+z_center, block_id))
                else:
                    if x > 0 and z > 0:
                        facing = 1
                    elif x > 0 and z < 0:
                        facing = 2 
                    elif x < 0 and z > 0:
                        facing = 3 
                    else:
                        facing = 4
                    print("/setblock {0} {1} {2} {3} {4}".format(
                        x+x_center, y, z+z_center, block_id, facing))



def tiered_structure(x_center, y_bottom, z_center, tiers,
                        greenspace_width, hardblock_id, fence_id, 
                        tier_height, clear_first=False, add_floors=True,
                        floor_id="minecraft:stone_slab"):
    """
    Generate a tiered structure with greenspace between tiers.


    Keyword arguments:
    x_center -- the center of the structure in the x dimension
    y_bottom -- the base of the structure in the y dimension
    z_center -- the center of the structure in the z dimension
    tiers -- the number of concentric tiers
    greenspace_width -- the width of the grass area between tiers
    hardblock_id -- the block type for the hard parts of the structure
    fence_id -- the block type for the fences of the structure
    tier_height -- the height of the wall for each tier
    clear_first -- should the area and surrounding area be cleared first
    add_floors -- should floors be created between levels
    floor_id -- the block type for the floors
    """

    if clear_first:
        # begin by filling the entire space with air blocks 4 beyond radius
        # and four up from top
        air_radius = ((greenspace_width+2) * (tiers)) + 4
        for y in range(tier_height*tiers + 4):
            for r in range(air_radius):
                circle_setblock(r, x_center, y + y_bottom, z_center,
                    "minecraft:air")

    # start from outside and work in
    y_current = y_bottom
    for tier in reversed(range(tiers)):
        # add 2 to greenspace for the hardblock, add 1 to tier
        # so that ring 0 has a radius
        radius = (greenspace_width+2) * (tier+1)
        # build wall
        for y_increment in range(tier_height):
            circle_setblock(radius, x_center, y_current, z_center,
                    hardblock_id)
            y_current += 1
        # grass section
        y = y_current - 1
        for r in range(radius-1, radius-1-greenspace_width, -1):
            circle_setblock(r, x_center, y, z_center, "minecraft:grass")
        # inner hardblock ring
        circle_setblock(radius-1-greenspace_width, x_center, y, z_center,
                hardblock_id)
        # floors, if any
        if add_floors:
            for r in range(radius-2-greenspace_width, 1, -1):
                circle_setblock(r, x_center, y, z_center,
                    floor_id)
        # spider proofing overhang
        circle_setblock(radius+1, x_center, y, z_center, hardblock_id)
        # fence
        circle_setblock(radius+1, x_center, y+1, z_center, fence_id)
        # torches
        # on top of fence
        circle_setblock(radius+1, x_center, y+2, z_center, "minecraft:torch",
                thin=True)
        # on side of overhang
        circle_setblock(radius-1-greenspace_width, x_center, y+1, z_center, "minecraft:torch",
                thin=True)


def main():
    parser = argparse.ArgumentParser(description="create commands for " +
                                        "modular tiered fortress")
    parser.add_argument("-x", "--x-center", type=int, required=True,
                        help="center of structure in x dimension")
    parser.add_argument("-z", "--z-center", type=int, required=True,
                        help="center of structure in z dimension")
    parser.add_argument("-y", "--y-bottom", type=int, required=True,
                        help="bottom of structure in y dimension")
    parser.add_argument("-t", "--tiers", type=int, required=True,
                        help="the number of tiers to make")
    parser.add_argument("-w", "--greenspace_width", type=int, required=True,
                        help="the width of the grass area between tiers")
    parser.add_argument("-b", "--hardblock_id", type=str, required=True,
                        help="the block id of the hard block")
    parser.add_argument("-f", "--fence_id", type=str, required=True,
                        help="the block id of the fence")
    parser.add_argument("-e", "--tier_height", type=int, required=True,
                        help="the height of the tiers")

    args = parser.parse_args()

    tiered_structure(args.x_center, args.y_bottom, args.z_center, args.tiers,
                        args.greenspace_width, args.hardblock_id,
                        args.fence_id, args.tier_height)


if __name__ == "__main__":
        main()
