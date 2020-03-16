from functools import lru_cache
from collections import defaultdict, Counter


def stacking_cubes(cubes):
    merged_cubes = []
    for k, v in Counter(cubes).items():
        x, y, h = k
        if h == 1:
            merged_cubes.append((x, y, h, h * v))
        else:
            for _ in range(v):
                merged_cubes.append((x, y, h, h))
    cubes = merged_cubes

    def is_stack(cube_1, cube_2):
        x1, y1, e1, _ = cube_1
        x2, y2, e2, _ = cube_2
        return (x2 <= x1 < x2 + e2 or x1 <= x2 < x1 + e1) and (y2 <= y1 < y2 + e2 or y1 <= y2 < y1 + e1)

    @lru_cache()
    def height(st):
        return sum(s[3] for s in st)

    def search(rest, stack):
        if not rest:
            return stack

        last = stack and stack[-1]

        max_stack = tuple(stack)
        for i, cube in enumerate(rest):
            if not last or is_stack(cube, last):
                rs = search(rest[:i] + rest[i + 1:], stack + [cube])
                if height(rs) > height(max_stack):
                    max_stack = rs

        return tuple(max_stack)

    result = search(cubes, [])
    # print(result)
    # return height(result)
    return height(tuple(result)), result


def select_drawing_cubes(cubes):
    normalized_cubes = []
    for cube in cubes:
        for _ in range(len(cube) == 3 or cube[3] // cube[2]):
            normalized_cubes.append((cube[:3]))
    cubes = normalized_cubes

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


if __name__ == '__main__':
    assert stacking_cubes(
        list(map(tuple,
        [[1, -4, 3], [5, 4, 3], [-8, 2, 1], [-3, 8, 1], [-2, -6, 3], [-3, 2, 4], [5, -5, 3], [-8, -3, 5], [-8, -7, 1],
         [-9, 4, 4], [3, -8, 5], [1, 8, 5], [5, 10, 3], [-3, 2, 4], [8, -8, 2], [10, -7, 1], [-3, 9, 2], [0, 7, 1],
         [2, 4, 3], [1, 9, 3]]))) == 11
    assert stacking_cubes(
        list(map(tuple, [[-7, -8, 5], [4, 1, 3], [2, -3, 4], [10, 2, 3], [3, 0, 4], [6, -9, 2], [6, -7, 5], [4, -3, 3],
                         [-6, 5, 4], [0, -1, 2], [8, -2, 5], [-5, -9, 1], [5, 10, 5], [1, 2, 3], [-4, -9, 5],
                         [-9, 4, 3], [10, 9, 1], [-8, 5, 5], [-2, 3, 1], [9, -2, 5]]))) == 19
    assert stacking_cubes(
        list(map(tuple,
                 [[-3, 6, 3], [6, -8, 5], [3, -6, 2], [3, -8, 3], [0, 0, 3], [2, -8, 4], [-1, -7, 1], [10, -1, 2],
                  [-8, -2, 2],
                  [6, -1, 2], [-6, -2, 1], [4, 7, 3], [-1, 1, 2], [-10, -10, 4], [0, 3, 3], [-7, 5, 3], [5, -9, 4],
                  [-10, -10, 2], [-10, 6, 5], [8, 8, 2], [-6, -5, 3], [-7, 0, 4], [6, 5, 1], [-9, 1, 3], [-4, -3, 2],
                  [0, -5, 4],
                  [-3, -3, 3], [4, -10, 1], [-8, -2, 5], [5, 2, 4]]))) == 22
    assert stacking_cubes(
        [(9, -1, 2), (-1, -9, 4), (1, -7, 5), (-1, 7, 1), (-3, 5, 2), (-1, -2, 5), (5, 4, 2), (-3, -10, 5),
         (-3, -10, 5), (9, -3, 1), (-2, -8, 1), (-10, -1, 1), (10, 10, 1), (5, -10, 1), (-4, -3, 2), (-4, 0, 2),
         (1, 6, 2), (-10, 2, 1), (3, -8, 3), (-1, -6, 5), (8, -1, 3), (1, 1, 5), (2, 0, 1), (-10, -8, 2), (-2, -2, 1),
         (7, 7, 2), (-5, -7, 3), (-7, -1, 4), (-8, 1, 4), (-1, -4, 5)]) == 49, 'test01'
