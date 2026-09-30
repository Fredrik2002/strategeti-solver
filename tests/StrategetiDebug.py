import copy


from src.pieces.Elephant import Elephant
from src.pieces.Gazelle import Gazelle
from src.utils.Constants import MAPPING_INDICES_BIT, MASK_POSITION_FOOTPRINT
from src.utils.Strategeti import Strategeti

game = Strategeti()

0b111111
fen = 0xfabc6008_0424_0800_0100
real_fen = fen << 1
real_fen |= 1

real_fen &= MASK_POSITION_FOOTPRINT
real_fen |= 0b111 << 65
print(hex(real_fen >> 1))