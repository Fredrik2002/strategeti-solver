# Strategeti Solver

## 📌 Description

The goal of the project is the solve the game Strategeti. This project is open to contribution

## 📖 Game rules
- 2 players
- 4x4 board
- A player won if :
  - 5 opponent pieces get captured
  - The opponent is out of moves
- Each player starts the game with 2 zebras, 2 gazelles, 2 elephant and 2 lions
- On each move, the player can choose to put a new piece on the board, 
or to move an existing one
- Pieces movement :
  - 🦓 Zebra can move in all 8 directions by one or more squares.
  It cannot jump over other pieces.
  - Gazelle moves by jumping over one or 2 pieces in all 8 directions. 
  It can concatenate multiple jumps in different 
  direction in one move, making its movements unpredictable
  - 🦁 Lion can move only by capturing a Zebra or a Gazelle one square up, down, left or right. 
  Player can capture its own pieces with a Lion
  - 🐘 Elephant push a pieces stack in all 4 directions. 
  The push is not available if another elephant is on the stack.
  If a piece gets pushed off the board, it is considered as captured.
  Elephant can push its own pieces

## ✨ Functionalities

* Solving the game from scratch :
  * This is achieved by performing a depth-first search from the beginning of the game
* Play a game using the database of solved positions 


## 🚀 Utilisation

- StrategetiTest solves the game using previously known positions in database.json. 
Removing or cleaning the file starts the soling from scratch


## 📁 Project structure

```text
projet/
├── src/
│   ├── pieces/
│   │     ├── Piece.py
│   │     ├── Elephant.py
│   │     ├── Gazelle.py
│   │     ├── Lion.py
│   │     └── Zebra.py
│   ├── utils/
│   │     ├── Player.py
│   │     ├── PositionStorage.py
│   │     └── Strategeti.py
│   └── StrategetiSolver.py
├── tests/
│   ├── BenchmarkDatabase.py
│   ├── ElephantTest.py
│   ├── GazelleTest.py
│   └── LionTest.py
└── README.md
```


## 📋 To do List :
- ### Performance improvements : The 2 major weak points are :
  - `get_position_as_integer2` : **40% of total running time**. Used to translate a position into an integer. It is called at each call to the database.
An improvement would be to modify the integer on each move instead of recreating it from scratch
  - `Gazelle.get_legal_moves` : **18.5% of total running time**. Used to compute the legal moves for a gazelle
at a given position. The complexity of the gazelle movements makes it hard to compute.
- ### Database storage efficiency :
  - Positions are stored in the database in a ~70 bits integer. The database is stored as python dictionary
dumped using `pickle`. Finding a way to represent a position with 64 bits or less should decently reduce
the disk size of the database (as well as the loading/dumping time ?)
- ### Symmetrical positions
  - There are 4 symmetry axes, due to the fact that we play on a 4x4 board, 
and the movement of the pieces is symmetrical. 
Which means that when a position is solved, it is also solved
for all its symmetric variants. 
However, this might divide the number of position by 4, and increase the database size
by as much. The gain might not be good enough.
The whole tree search needs to be optimized to not reach any symetrical positions




