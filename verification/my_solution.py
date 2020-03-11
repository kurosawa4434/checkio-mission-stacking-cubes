from functools import lru_cache
from collections import defaultdict


def select_drawing_cubes(cubes):
    def make_serface_cubes(x, y, z, e):
        cubes = set()
        for dx in range(e):
            for dz in range(e):
                cubes.add((x + dx, y + (e - 1), z + dz))
        for dx in range(e):
            for dy in range(e - 1):
                cubes.add((x + dx, y + dy, z))
        for dz in range(e):
            for dy in range(e - 1):
                cubes.add((x + (e - 1), y + dy, z + dz))
        return cubes

    h = 0
    draw_cubes = []
    for x, y, e in cubes:
        draw_cubes.append([x, h, y, e])
        h += e

    sliced_surface_cubes = set()
    for c in draw_cubes:
        sliced_surface_cubes |= make_serface_cubes(*c)

    same_2d_coord_cubes = defaultdict(list)
    for x, y, z in sliced_surface_cubes:
        cs = (x + z, y + (z - x) // 2)
        same_2d_coord_cubes[cs].append((x, y, z))

    # select top cube in the same 2d position
    drawing_cubes = set()
    for s in same_2d_coord_cubes.values():
        drawing_cubes.add(sorted(s, key=lambda co: co[1])[-1])

    # remove hidden cubes and faces
    result_cubes = []
    for x, y, z in drawing_cubes:
        if {(x, y + 1, z), (x + 1, y, z), (x, y, z - 1)} <= drawing_cubes:
            continue
        # top
        top = int((x, y + 1, z) not in drawing_cubes)
        # left
        left = int((x, y, z - 1) not in drawing_cubes)
        # right
        right = int((x + 1, y, z) not in drawing_cubes)

        result_cubes.append((x, z, y, top, left, right))

    return result_cubes


def stacking_cubes(cubes):
    def is_stack(cube_1, cube_2):
        x1, y1, e1 = cube_1
        x2, y2, e2 = cube_2
        if x2 <= x1 < x2 + e2 or x1 <= x2 < x1 + e1:
            if y2 <= y1 < y2 + e2 or y1 <= y2 < y1 + e1:
                return True
        return False

    @lru_cache()
    def height(st):
        return sum(s[2] for s in st)

    def search(rest, stack, max_stack):
        last = stack[-1]
        if not rest:
            return stack

        new_max_stack = list(max_stack)
        for i, cube in enumerate(rest):
            if is_stack(cube, last):
                rs = search(rest[:i] + rest[i + 1:], stack + [cube], max_stack)
                if height(tuple(rs)) > height(tuple(new_max_stack)):
                    new_max_stack = rs

        return new_max_stack or stack

    result = search(cubes, [(-1000, -1000, 2000)], [])
    return height(tuple(result)) - 2000
