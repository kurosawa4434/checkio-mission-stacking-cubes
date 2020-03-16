"""
TESTS is a dict with all of your tests.
Keys for this will be the categories' names.
Each test is a dict with
    "input" -- input data for a user function
    "answer" -- your right answer
    "explanation" -- not necessarily a key, it's used for an additional info in animation.
"""
from my_solution import stacking_cubes, select_drawing_cubes
from random import shuffle, randint


def make_test_dic(input, answer, explanation):
    return {
        'input': input,
        'answer': answer,
        'explanation': explanation,
    }


def make_basic_tests(inputs):
    basic_tests = []
    for inp, answer, order in inputs:
        explanation = select_drawing_cubes([inp[o] for o in order])
        shuffle(inp)
        basic_tests.append({'input': inp,
                            'answer': answer,
                            'explanation': explanation})
    return basic_tests


def make_random_tests(num):
    random_tests = []
    for _ in range(num):
        input_cubes = []
        for _ in range(20):
            input_cubes.append((randint(-10, 10), randint(-10, 10), randint(1, 5)))
        answer, answer_cubes = stacking_cubes(input_cubes)
        random_tests.append({
            'input': input_cubes,
            'answer': answer,
            'explanation': select_drawing_cubes(answer_cubes),
        })
    return random_tests


TESTS = {
    "Basics": make_basic_tests([
        # basic
        [
            [
                (0, 0, 2),
                (1, 1, 2),
                (3, 2, 2),
            ],
            4,
            range(2),
        ],
        # select 1
        [
            [
                (0, 0, 2),
                (1, 1, 2),
                (2, 2, 2),
                (1, 2, 1),
            ],
            6,
            range(3),
        ],
        # select 2
        [
            [
                (0, 0, 2),
                (0, 0, 2),
                (2, 0, 2),
                (2, 0, 2),
                (2, 0, 2),
                (0, 2, 2),
                (0, 2, 2),
                (0, 2, 2),
                (0, 2, 2),
            ],
            8,
            range(5, 9),
        ],
        # no stacking
        [
            [
                (0, 0, 2),
                (0, 3, 2),
                (3, 0, 2),
            ],
            2,
            [0, ]
        ],

        # negative coordinates
        [
            [
                (0, 0, 2),
                (-1, -1, 2),
                (-2, -2, 2),
            ],
            6,
            range(3),
        ],
    ]),
    "Extra": make_basic_tests([
        # icon
        [
            [
                (-2, -1, 3),
                (-1, 0, 2),
            ],
            5,
            range(2),
        ],
        # spiral
        [
            [
                (0, 0, 1),
                (0, 0, 2),
                (1, 1, 2),
                (0, 2, 2),
                (-1, 2, 2),
                (-3, 0, 3),
                (-3, -2, 3),
                (-1, -4, 3),
                (1, -3, 3),
                (3, -1, 3),
                (3, 1, 4),
            ],
            28,
            range(11),
        ],

        # stair
        [
            [
                (i, 0, 2) for i in range(10)
            ] + [
                (9, i + 1, 2) for i in range(10)
            ] + [
                (8 - i, 10, 2) for i in range(10)
            ] + [
                (-1, 9 - i, 2) for i in range(8)
            ],
            10 * 2 * 3 + 8 * 2,
            range(10 * 3 + 8),
        ],
        # Escher
        [
            [
                (2, 2, 1),
                (2, 2, 1),
                (-4, -4, 7),
                (-3, -3, 1),
                (-3, -3, 1),
                (-3, -3, 1),
                (-3, -3, 1),
                (-3, -3, 1),
                (-3, -3, 5),
                (0, 0, 1),
                (0, 0, 1),
                (0, 0, 1),
                (-2, -2, 3),
                (-2, 0, 1),
                (-2, 0, 1),
            ],
            27,
            range(15),
        ],
    ]),
    'Randoms': make_random_tests(8),
}
