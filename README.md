# ❌🅾️ Python Tic-Tac-Toe (Console Game)

A fully functional, robust Tic-Tac-Toe game featuring both Command Line (CLI) and Graphical (GUI) interfaces. The project supports 1-player (vs AI) and 2-player modes, multiple AI difficulty levels, and adheres to strict modern Python standards.

This project serves as a practical playground for mastering Python architecture, design patterns, and software engineering best practices.

## Table of Contents

1. [Architectural Principles](#architectural-principles)
2. [How to Run the Game](#how-to-run-the-game)
3. [Testing Instructions](#testing-instructions)
4. [Features](#features)
5. [Development Standards](#development-standards)
6. [Learning Journey & Roadmap](#learning-journey--roadmap)
7. [License](#license)

## Architectural Principles

This project demonstrates clean Python architecture, enforcing a strict Model-View-Controller (MVC) pattern and Test-Driven Development (TDD).

-   **Model (Core & Players):** The `GameEngine` manages state, rules, and win logic. It is entirely decoupled from the UI. AI logic (Minimax, Strategic) is encapsulated in the `src.players` package.
-   **View (UI):** Abstracted via `AbstractView`. Implementations include `CLIView` (console I/O) and `GUIView` (Tkinter), which handle rendering and user input without containing game logic.
-   **Controller:** The `AbstractController` orchestrates the flow. It binds the Model and View, ensuring the game loop functions regardless of the interface used.
-   **Dependency Injection:** Components (like the Engine into the View, or the View into the Controller) are injected to ensure loose coupling and high testability.
-   **Robust Testing:** Every major component is unit-tested using Python's `unittest` module, including techniques like mocking user input to ensure reliability.

## How to Run the Game

The game requires Python 3.10+ (due to modern PEP 604 type hinting).

### 1. Launching the Game

Navigate to the root directory and run `main.py`.

**Command Line Interface (Default):**

```bash
python main.py
```

**Graphical User Interface:**

```bash
python main.py --gui
```

### 2. Gameplay Instructions

-   Setup: Follow the prompts to select 1-player or 2-player mode, markers, and AI difficulty.
-   AI Difficulties:
    -   Easy: Random moves.
    -   Medium: Wins if possible.
    -   Hard: Wins if possible, blocks opponent wins.
    -   Impossible: Minimax algorithm (Perfect play).

## Testing Instructions

This project maintains high test coverage using Python's `unittest` and `unittest.mock` libraries.

### Running the Suite

From the root directory

```bash
python -m unittest discover -b
```

### Test Organization

The `tests/` directory mirrors the `src/` structure:

-   `test_core/`: Engine logic and factory validation.
-   `test_controllers/`: Game loop and setup logic (isolated via mocks).
-   `test_players/`: AI strategies and input validation.
-   `test_views/`: UI rendering and formatting logic.

## Features

-   ✅ **Dual Interface:** Switch seamlessly between CLI and GUI.
-   ✅ **Robust AI:** 4 distinct difficulty levels, including an unbeatable Minimax bot.
-   ✅ **MVC Architecture:** Clean separation of concerns.
-   ✅ **Type Safety:** Full PEP 484/585/604 type hinting coverage.
-   ✅ **Google-Style Docs:** Comprehensive docstrings for all modules and classes.

## Development Standards

This project enforces strict code quality rules:

-   **Linting:** Compliant with Ruff default rules.
-   **Formatting:** Line length limited to 100 characters.
-   **Documentation:** All docstrings follow the Google Style Guide.
-   **Typing:** Uses modern built-in generics (`list[str]`) and union operators (`int | None`).

## Learning Journey & Roadmap

This project is built with the explicit goal of learning specific software domains. The table below tracks the implementation of these concepts, serving as a record of the architectural evolution of the application.

🟢 = Finished&nbsp;&nbsp;&nbsp;&nbsp;🟡 = In progress&nbsp;&nbsp;&nbsp;&nbsp;🔴 = Not started

---

| Status | Feature / Domain       | Technical Goal (Learning Objective)                                              | Architectural Impact                                                |
| ------ | ---------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| 🟡     | Multi-Tier AI Opponent | Master algorithmic thinking: Random Selection vs Heuristic Algorithms (Minimax). | AbstractAIPlayer hierarchy. AI requests live state from GameEngine. |

-   🟢 **Base Minimax**

    -   **Goal:** Random Selection vs Minimax
    -   **Impact:** AbstractAIPlayer hierarchy. AI requests live state from GameEngine.

-   🔴 **Improved Minimax**

    -   **Goal:** Add caching and alpha/beta pruning for efficiency
    -   **Impact:** Requires memoization structures and pruning logic

-   🔴 **Machine Learning AI**
    -   **Goal:** Adaptive difficulty with ML models
    -   **Impact:** Introduces ML pipeline integration and modular inference

<br>

| Status | Feature / Domain         | Technical Goal (Learning Objective)                     | Architectural Impact                                              |
| ------ | ------------------------ | ------------------------------------------------------- | ----------------------------------------------------------------- |
| 🟡     | Graphical User Interface | Explore HCI and Event-Driven Programming using Tkinter. | AbstractView interface. Hot-swapping between CLIView and GUIView. |

-   🟡 **Tkinter Desktop View**

    -   **Goal:** Event-driven programming with AbstractView interface
    -   **Impact:** Hot-swapping between CLIView and GUIView

-   🔴 **Cross-Platform Views**

    -   **Goal:** Extend GUIView to web, mobile, VR
    -   **Impact:** Requires abstract rendering layer and new frameworks

-   🔴 **Responsive Design**
    -   **Goal:** Adaptive layouts and UX patterns
    -   **Impact:** Introduces dynamic scaling and input abstraction

<br>

| Status | Feature / Domain      | Technical Goal (Learning Objective)                                             | Architectural Impact                                   |
| ------ | --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 🔴     | Persistent Statistics | Explore data persistence (SQL/SQLite). Learn data modeling and CRUD operations. | Persistence Layer separates DB logic from game engine. |

-   🔴 **SQL/SQLite CRUD**

    -   **Goal:** Learn data modeling and CRUD operations
    -   **Impact:** Persistence Layer separates DB logic from game engine

-   🔴 **Analytics Reports**
    -   **Goal:** Generate player performance summaries
    -   **Impact:** Requires reporting module and query optimization

<br>

| Status | Feature / Domain          | Technical Goal (Learning Objective)                                                      | Architectural Impact                                          |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| 🔴     | Local Network Multiplayer | Deep dive into networking protocols (TCP/IP) for reliable data transfer (Client/Server). | src/networking/ package. Game loop re-engineered for latency. |

-   🔴 **TCP/IP Protocols**

    -   **Goal:** Reliable client/server data transfer
    -   **Impact:** src/networking/ package. Game loop re-engineered for latency

-   🔴 **State Sync**
    -   **Goal:** Handle synchronization across clients
    -   **Impact:** Requires reconciliation logic and rollback strategies

<br>

| Status | Feature / Domain        | Technical Goal (Learning Objective)                                                | Architectural Impact       |
| ------ | ----------------------- | ---------------------------------------------------------------------------------- | -------------------------- |
| 🔴     | Real-Time Communication | Explore asynchronous programming (asyncio) for non-blocking features (e.g., chat). | Shift to non-blocking I/O. |

-   🔴 **Async Chat**

    -   **Goal:** Non-blocking chat features
    -   **Impact:** Requires shift to async I/O

-   🔴 **Notifications**
    -   **Goal:** Real-time alerts (turns, events)
    -   **Impact:** Requires event bus and concurrency-safe handlers

<br>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
