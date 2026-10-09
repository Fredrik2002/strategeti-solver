
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

class Constants:

    def __init__(self, N):
        # Corner squares are excluded (indices 0, 3, 12, 15)
        self.SQUARES_INDICES_NO_CORNER = [(x, y) for y in range(N) for x in range(N) if x not in [0, N-1] or y not in [0, N-1]]

        # Given a square, it returns the corresponding bit position in the footprint
        self.MAPPING_INDICES_BIT = [[(N * x + y) * 4 + 1 for y in range(N)] for x in range(N)]

        # Given a square, it clears the bits at the position corresponding to the square in the footprint
        self.CLEAR_MAPPING_INDICES_BIT = [[~(0b1111 << self.MAPPING_INDICES_BIT[x][y]) for y in range(N)] for x in range(N)]

        # For a given square and piece, it returns the piece id shifted to the correct number of bits
        self.SET_MAPPING_INDICES_BIT = [[[piece << self.MAPPING_INDICES_BIT[x][y] for piece in range(1, 9)] for y in range(N)] for x in range(N)]

        self.FOOTPRINT_BIT_SHIFT = {
            "z" : 4*N*N + 1,
            "Z" : 4*N*N + 3,
            "g" : 4*N*N + 5,
            "G" : 4*N*N + 7,
            "l" : 4*N*N + 9,
            "L" : 4*N*N + 11,
        }

        # GAZELLE MOVEMENTS
        # For each square, we store the neighboor squares
        self.NEIGHBOOR = [[[] for _ in range(N)] for _ in range(N)]

        for x in range(N):
            for x_offset in range(-1, 2):
                new_x = x + 2 * x_offset
                if 0 <= new_x < N:
                    for y in range(N):
                        for y_offset in range(-1, 2):
                            if 0 <= y + 2 * y_offset < N and (x_offset, y_offset) != (0, 0):

                                first_neighboor = x + x_offset, y + y_offset
                                second_neighboor = x + 2 * x_offset, y + 2 * y_offset
                                third_neighboor = x + 3 * x_offset, y + 3 * y_offset

                                # Third neighboor checking
                                if not (0 <= x + 3 * x_offset < N and 0 <= y + 3 * y_offset < N):
                                    third_neighboor = None

                                self.NEIGHBOOR[x][y].append((first_neighboor, second_neighboor, third_neighboor))

        # ZEBRA MOVEMENTS
        self.ZEBRA_DIAGS = [[[] for _ in range(N)] for _ in range(N)]

        for x in range(N):
            for y in range(N):
                for x_offset in [-1, 1]:
                    for y_offset in [-1, 1]:
                        coeff = 1
                        if 0 <= x + x_offset * coeff < N and 0 <= y + y_offset * coeff < N:
                            self.ZEBRA_DIAGS[x][y].append([])
                        while 0 <= x + x_offset * coeff < N and 0 <= y + y_offset * coeff < N:
                            self.ZEBRA_DIAGS[x][y][-1].append((x + x_offset * coeff, y + y_offset * coeff))
                            coeff += 1