# Strategeti Solver

## 📌 Description

The goal of the project is the solve the game Strategeti. This project is open to contribution

## 📖 Game rules
- 2 players
- 4x4 board (configurable to smaller)
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

### 1. Solving mechanism
  * This is achieved by performing a tree search from the beginning of the game
  

#### 1.1. Storing the positions 
  * Positions are stored as an integer with the bits carrying the information :
    - 1 bit for the player's turn
    - 4 bits for each square of the board (8 different pieces + empty square)
    - 2 bits for each type of piece, the number of times it is captured (between 0 and 2)
    - 2 bits for the number of times the position was reached
    Which gives a total of :
      - 3x3 board : 1 + 36 + 16 = 53 bits
      - 4x4 board : 1 + 64 + 16 = 81 bits
#### 1.2. Evaluating a position 
  - The evaluation of a position is a tuple (finished, evaluation) :

| Finished | Evaluation |                                                                Explanation |
|:--------:|:----------:|---------------------------------------------------------------------------:|
|    1     |     1      |                                            The game is finished, white won |
|    1     |     -1     |                                            The game is finished, black won |
|    1     |     0      | The game is finished, draw (draw can only occur if a position is repeated) |
|    0     |    $x$     |                  The game is still ongoing, but white can win in $x$ moves |
|    0     |    $x$     |                  The game is still ongoing, but black can win in $x$ moves |
|    0     |     0      |            The game is still ongoing, but the game should end up in a draw |
  - Knowing the evaluations of all the subpositions means that we can evaluate the current position, 
using the **minimax algorithm**

### 2. Playing mechanism
* Play a game using the database of solved positions which indicates which are the best moves


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

## 🏎️ Benchmark (4x4 board) :

- ### 🌳 Tree search global efficiency :
| Date  | Number of position solved | Duration (in s) | Ratio (avg number of position solved per second | Improvements                                                  |
|-------|--------------------------:|----------------:|------------------------------------------------:|---------------------------------------------------------------|
| 29/09 |                   376 482 |          60.201 |                                           6 253 |                                                               |
| 30/09 |                   502 941 |          60.758 |                                           8 277 | Modify the FEN on the fly for 'Move'                          |
| 30/09 |                   567 780 |          60.160 |                                           9 437 | Modify the FEN on the fly for 'Place & new gazelle movements' |

- ### 🔧 Function calls efficiency :
| Function name                               | Number of call | Percentage of total running time |
|---------------------------------------------|---------------:|---------------------------------:|
| Strategeti.py:193(get_position_as_integer2) |        6569398 |                            14.1% |
| Gazelle.py:9(get_legal_moves)               |        1532716 |                            13.5% |
| Player.py:53(make_move)                     |         689728 |                             8.7% |
| Piece.py:73(cancel_move)                    |        4812599 |                             6.8% |

### Number of positions :
| Board size | Number of pieces (E, G, L, Z) per player | Number of positions |
|------------|-----------------------------------------:|--------------------:|
| 3x3        |                           4 (1, 1, 1, 1) |           3 719 282 |


## 📋 To-Do List & Future Improvements

### 🔄 Handle Cycles in the Tree Search

* Currently, positions are stored alongside the number of times they have appeared in the game history. This prevents cycles from occurring in the search tree and simplifies the algorithm.
* However, this approach significantly increases the number of stored positions, as the same board configuration can be stored multiple times depending on its occurrence count.
* **Goal:** Find a more efficient way to handle repetitions without unnecessarily increasing the number of stored positions.

### ⚡ Performance Optimization

* Identify and optimize the two main performance bottlenecks in the solver.
* **Goal:** Reduce the overall solving time through profiling and targeted optimizations.

### 🌳 Tree Search Improvements

* Explore techniques to accelerate the tree search by leveraging relationships between similar positions.
* For example, if White wins because Black has no legal moves, small modifications to the position might reveal other winning positions without requiring a complete search.
* **Goal:** Reduce the number of positions that need to be explored by reusing previously discovered results.

### 💾 Database Storage Efficiency

* The database is currently stored as a Python dictionary and serialized using `pickle`.
* The goal is to find a more language-independent storage format that further reduces database size and improves serialization and deserialization times.
* **Goal:** Minimize storage requirements while speeding up database loading and saving.

### 📊 Estimate the Number of Reachable Positions

* Investigate mathematical or computational methods to establish bounds on the number of reachable positions.
* **Goal:** Estimate the total number of positions that need to be solved and, consequently, the time required to solve a given version of the game.

### 📈 Performance Visualization

* Plot the number of positions solved over successive 100 ms intervals.
* This should help visualize how the solver's throughput evolves as the database grows and identify potential performance degradation.
* **Goal:** Better understand the relationship between database size and solving speed.

### 🚀 Port the Solver to C++

* Python is becoming a limiting factor as the computational workload increases. Porting the solver to C++ could significantly reduce solving times.
* However, this should be done only after exhausting the most promising optimization opportunities in the Python implementation.
* **Goal:** Maximize performance while avoiding a premature rewrite.






