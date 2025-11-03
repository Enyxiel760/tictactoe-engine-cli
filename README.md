# ❌🅾️ Python Tic-Tac-Toe (Console Game)

This is a fully functional, turn-based, two-player game of Tic-Tac-Toe designed to run directly in the command line. 



## Table of Contents

1. [Architectural Principles](#architectural-principles)
2. [How to Run the Game](#how-to-run-the-game)
3. [Testing Instructions](#testing-instructions)
5. [Future Development & Learning Roadmap](#future-development--learning-roadmap)
6. [License](#license)



## Architectural Principles

This project serves as an exercise in clean Python development, focusing on the following architectural principles:

* **Encapsulated State (OOP):** The entire game state (the board, current player, and turn order) is **encapsulated** within the **`GameEngine` class**. The engine is responsible for safely and atomically **mutating** the board state upon valid moves.
* **Polymorphic Player Design:** All players (Human, AI, Networked) adhere to a unified `AbstractPlayer` interface, allowing the `GameEngine` to request a move without caring how that move is generated (Ask, Don't Tell principle).
* **Separation of Concerns:** The architecture is layered: **Engine** (State/Rules), **Players** (Input/Decision Logic).
* **Robust Testing:** Every major component is unit-tested using Python's `unittest` module, including techniques like mocking user input to ensure reliability.



## How to Run the Game

This game runs directly in your command-line environment and requires no external dependencies beyond the standard Python library.

### Prerequisites

* **Python 3.6+**

### Execution

1.  Navigate to the **root directory** of the project (the folder containing the `src/` and `tests/` directories).
2.  Execute the game using the following command:

    ```bash
    python src/main.py
    ```

    The game will start immediately, display the position guide, and prompt the first player ('X') for a move.



## Testing Instructions

This project is built using a Test-Driven Development (TDD) approach, with every function verified by unit tests.

### How to Run Tests

1.  Ensure you are in the project's **root directory** (the folder containing `src/` and `tests/`).
2.  Execute the test suite using Python's built-in `unittest` module with the `discover` and `buffer` flags:

    ```bash
    python -m unittest discover -b
    ```

    * **`discover`** automatically finds all files named `test*.py`.
    * **`-b` (buffer)** silences all the `print` output (like error messages from mocked input) from successful tests, keeping the test run clean.

### Expected Output

A successful test run will be silent, showing only the final summary indicating the number of tests run and that everything passed.



## Future Development & Learning Roadmap

This project currently serves as a core demonstration of clean Python architecture and robust unit testing. The game engine logic has been strictly isolated to provide a solid, class-based, encapsulated foundation for extensive expansion.

The ideas below represent potential paths for exploration and learning. They are not commitments, but rather opportunities to tackle new domains of software development and showcase expanding skills.

### Key Expansion and Learning Goals

| Feature Idea | Technical Goal (What to Learn) | Architectural Impact |
| :------------------------------- | :--- | :--- |
| **Multi-Tier AI Opponent**       | Master algorithmic thinking by building AI difficulties: from Random Selection to Heuristic Algorithms (e.g., Minimax). | Requires a Player Hierarchy. New AI classes inherit from AbstractAIPlayer, requesting the live state from the injected GameEngine instance to calculate moves. |
| **Advanced User Interface (UX)** | Explore human-computer interaction (HCI) concepts. Goals range from basic CLI enhancements (color, ASCII art flair) to full-scale Graphical User Interface (GUI) development (e.g., using Tkinter, PyQt, or a browser-based front-end). | Introduces a new layer of presentation logic. The existing `prettify_board()` function will be replaced or supplemented by new renderers that consume the state from the `GameEngine`'s public interface. |
| **Persistent Player Statistics** | Explore data persistence by integrating a database layer. This involves learning about data modeling, relational schemas, and general CRUD (Create, Read, Update, Delete) operations. | Requires a new Persistence Layer that separates database logic from the game engine. New files would handle database connection, queries, and data mapping. |
| **Local Network Multiplayer**    | Deep dive into networking protocols, specifically TCP/IP for connection handling and reliable data transfer. The goal is to separate the CLI interface into distinct Client and Server applications. | Requires a new `src/networking/` package. The game loop in `main.py` would need to be re-engineered to handle latency and state synchronization across two machines. |
| **Real-Time Communication**      | Explore asynchronous programming concepts (e.g., `asyncio`). The objective is to manage a persistent, low-latency communication channel (for features like in-game chat) without blocking the core game's execution flow. | Introduces new challenges in concurrency and handling simultaneous data streams, requiring deep knowledge of non-blocking I/O. |


### Architectural Focus Moving Forward

Every feature added will reinforce the project's original principles:
* **Encapsulated State**: The core engine's state is mutated only through controlled methods (make_move), ensuring new features consume the state via public getters but do not bypass the engine's internal rules.
* **Testing**: New modules (AI, DB, Network) will be covered by their own comprehensive unit and integration tests.
* **Separation of Concerns**: Maintaining strict boundaries between Game Engine (logic), Persistence (database), and I/O (CLI/Network).

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
