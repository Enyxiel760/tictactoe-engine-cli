# ❌🅾️ Python Tic-Tac-Toe (Console Game)

---

This is a fully functional, turn-based, two-player game of Tic-Tac-Toe designed to run directly in the command line. This project serves as an exercise in clean Python development, focusing on the following architectural principles:

* **Immutability:** The core game state is maintained without mutation; every move returns a brand new copy of the board.
* **Separation of Concerns:** Logic (checking winner, validating moves) is kept separate from I/O (getting input, rendering the board).
* **Robust Testing:** Every major component is unit-tested using Python's `unittest` module, including techniques like mocking user input to ensure reliability.

---

## 🚀 How to Run the Game

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

---

## ✅ Testing Instructions

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

A successful test run will be silent, showing only the final summary (the number of dots will correspond to the total number of tests):