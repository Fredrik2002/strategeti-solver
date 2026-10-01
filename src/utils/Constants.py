
# 16 squares * 4 bits + 1 bits for player's turn
MASK_POSITION_FOOTPRINT = 0x1ffffffffffffffff

# Corner squares are excluded (indices 0, 3, 12, 15)
SQUARES_INDICES_NO_CORNER = [
    (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2), (1, 3),
    (2, 0), (2, 1), (2, 2), (2, 3),
    (3, 1), (3, 2),
]

MAPPING_INDICES_BIT = [[(4 * x + y) * 4 + 1 for y in range(4)] for x in range(4)]

CLEAR_MAPPING_INDICES_BIT = [[~(0b1111 << MAPPING_INDICES_BIT[x][y]) for y in range(4)] for x in range(4)]

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

SET_MAPPING_INDICES_BIT = [[[piece << MAPPING_INDICES_BIT[x][y] for piece in range(1, 9)] for y in range(4)] for x in range(4)]

FOOTPRINT_BIT_SHIFT = {
    "z" : 65,
    "Z" : 67,
    "g" : 69,
    "G" : 71,
    "l" : 73,
    "L" : 75
}

# GAZELLE MOVEMENTS
# For each square, we store the neighboor squares
NEIGHBOOR = [[[] for _ in range(4)] for _ in range(4)]

for x in range(4):
    for x_offset in range(-1, 2):
        new_x = x + 2 * x_offset
        if 0 <= new_x <= 3:
            for y in range(4):
                for y_offset in range(-1, 2):
                    if 0 <= y + 2 * y_offset <= 3 and (x_offset, y_offset) != (0, 0):

                        first_neighboor = x + x_offset, y + y_offset
                        second_neighboor = x + 2 * x_offset, y + 2 * y_offset
                        third_neighboor = x + 3 * x_offset, y + 3 * y_offset

                        # Third neighboor checking
                        if not (0 <= x + 3 * x_offset <= 3 and 0 <= y + 3 * y_offset <= 3):
                            third_neighboor = None

                        NEIGHBOOR[x][y].append((first_neighboor, second_neighboor, third_neighboor))

# ZEBRA MOVEMENTS
ZEBRA_DIAGS = [[[] for y in range(4)] for x in range(4)]

for x in range(4):
    for y in range(4):
        for x_offset in [-1, 1]:
            for y_offset in [-1, 1]:
                coeff = 1
                if 0 <= x + x_offset * coeff <= 3 and 0 <= y + y_offset * coeff <= 3:
                    ZEBRA_DIAGS[x][y].append([])
                while 0 <= x + x_offset * coeff <= 3 and 0 <= y + y_offset * coeff <= 3:
                    ZEBRA_DIAGS[x][y][-1].append((x + x_offset * coeff, y + y_offset * coeff))
                    coeff += 1