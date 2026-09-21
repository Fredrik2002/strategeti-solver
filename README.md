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

- StrategiTest solves the game using previously known positions in database.json. 
Removing or cleaning the file starts the soling from scratch


## 📁 Structure du projet

```text
projet/
├── src/
│   ├── main.cpp
│   └── ...
├── include/
│   └── ...
├── tests/
│   └── ...
├── README.md
└── CMakeLists.txt
```


## 📋 To do List :
- ### Database performance analysis.

At the moment, database is stored as a dictionary dumped into a pickle file. On a 14M element DB :

| --- | JSON | Pickle (Highest protocol) |
| --- | --- |---------------------------|
| Loading time (in s) | 45.18 ❌| 36.11 ✅                   | 
| Dumping time (in s) | 80.29 ❌| 19.69 ✅                   | 
| DB size (in Mb) |   663.8 ❌| 543.3 ✅                   | 
| Readibility | ✅ | ❌                         |

The main goal is to reduce the size of the DB, which will reduce loading time. 
The positions are currently stored as a string such as `0|GGLLZglzz|ZE___gE__e_l__e_1`. A first study would be 
to store such a string into an integer. That should drastically reduce the database size on the disk, but the loading step
will need to convert back every key integer entry into a string. It is unclear whether this is worth it or not



