
# Corner squares are excluded (indices 0, 3, 12, 15)
SQUARES_INDICES_NO_CORNER = [
    (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2), (1, 3),
    (2, 0), (2, 1), (2, 2), (2, 3),
    (3, 1), (3, 2),
]

MAPPING_INDICES_BIT = [[(4 * x + y) * 4 + 1 for y in range(4)] for x in range(4)]

MAPPING_PIECE_INTEGER = {
    "E" : 8,
    "G" : 1,
    "L" : 2,
    "Z" : 3,
    "e" : 4,
    "g" : 5,
    "l" : 6,
    "z" : 7,
    " " : 0
}