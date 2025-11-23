"""Entry point for the Tic Tac Toe application.

This module initializes the game by instantiating the appropriate controller and starting the
execution loop.
"""

import argparse
import sys

from src.controllers import AbstractController, CLIController, GUIController


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments to determine game configuration.

    Returns:
        argparse.Namespace: The parsed arguments containing user preferences.
    """
    parser = argparse.ArgumentParser(description="Play Tic Tac Toe.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help=(
            "Launch the Graphical User Interface (GUI) instead of the Command Line Interface (CLI)."
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Initialize and run the game application.

    Parses arguments to decide whether to launch the CLI or GUI controller.
    """
    args = parse_arguments()
    controller: AbstractController

    if args.gui:
        try:
            controller = GUIController()
        except Exception as e:
            # Fallback logic or error reporting if Tkinter isn't available or fails
            print(f"Error: Failed to initialize GUI ({e}).")
            sys.exit(1)
    else:
        controller = CLIController()

    controller.run()


if __name__ == "__main__":
    main()
