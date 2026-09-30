import copy


from src.pieces.Elephant import Elephant
from src.pieces.Gazelle import Gazelle
from src.utils.Constants import MAPPING_INDICES_BIT
from src.utils.Strategeti import Strategeti

game = Strategeti()


for i in range(16):
    fen = 0x1236_1344_4444_8861
    fen = fen << 1
    fen &= ~(0b1111 << MAPPING_INDICES_BIT[i])
    fen |= (0xa << MAPPING_INDICES_BIT[i])
    print(hex(fen >> 1))