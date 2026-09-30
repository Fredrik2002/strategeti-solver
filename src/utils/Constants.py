
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

# For each square, we store the neighboor squares
NEIGHBOOR = [[[] for _ in range(4)] for _ in range(4)]

# x, y, x_offset, y_offset -> first_neighboor, second_neighboor, third_neighboor
NEIGHBOORS_DESTINATION = [[[[[] for _ in range(3)] for _ in range(3)] for _ in range(4)] for _ in range(4)]

for x in range(4):
    for x_offset in range(-1, 2):
        new_x = x + 2 * x_offset
        if 0 <= new_x <= 3:
            for y in range(4):
                for y_offset in range(-1, 2):
                    if 0 <= y + 2 * y_offset <= 3 and (x_offset, y_offset) != (0, 0):
                        NEIGHBOOR[x][y].append((x_offset, y_offset))

                        first_neighboor = x + x_offset, y + y_offset
                        second_neighboor = x + 2 * x_offset, y + 2 * y_offset
                        third_neighboor = x + 3 * x_offset, y + 3 * y_offset

                        # Third neighboor checking
                        if not (0 <= x + 3 * x_offset <= 3 and 0 <= y + 3 * y_offset <= 3):
                            third_neighboor = None

                        NEIGHBOORS_DESTINATION[x][y][x_offset][y_offset] = (first_neighboor, second_neighboor, third_neighboor)