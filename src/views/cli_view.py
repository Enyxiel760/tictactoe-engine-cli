"""CLI view implementation for Tic Tac Toe.

Handles user input and board rendering for a command-line Tic-Tac-Toe game.
"""

from textwrap import dedent

from src.core import PlayerType
from src.views.abstract_view import AbstractView


class CLIView(AbstractView):
    """Handles user input and board rendering for a command-line Tic-Tac-Toe game.

    Provides validated input prompts for player setup and AI difficulty selection,
    and renders the game board in a human-readable format.
    """

    def _get_human_name(self) -> str:
        """Prompt the user to enter their name.

        Keeps asking until a non-empty string is provided.

        Returns:
            str: The user's name.
        """
        while True:
            name = input("What is your name? ").strip()
            if name:
                return name
            else:
                print("Name cannot be empty. Please try again.")

    def _choose_marker(self) -> str:
        """Prompt the user to choose a marker: 'X' or 'O'.

        Input is case-insensitive and validated.

        Returns:
            str: The chosen marker ('X' or 'O').
        """
        while True:
            prompt = "Do you want to be 'X' or 'O'? "
            choice = input(prompt).strip().upper()

            if choice == "X" or choice == "O":
                return choice
            else:
                print("Invalid choice. Please enter 'X' or 'O'.")

    def _choose_ai_difficulty(self) -> str:
        """Display a list of AI difficulty levels and prompt the user to choose one.

        Validates input against the keys in AI_DIFFICULTIES.

        Returns:
            str: The chosen difficulty level key.
        """
        min_key = PlayerType.get_min_difficulty_key()
        max_key = PlayerType.get_max_difficulty_key()

        valid_ai_keys = []
        prompt_lines = ["Choose your opponent's difficulty:"]

        for key, description in PlayerType.get_ai_options():
            valid_ai_keys.append(key)
            prompt_lines.append(f"  {key}) {description}")

        prompt_text = "\n".join(prompt_lines) + f"Enter your choice ({min_key}-{max_key}): "

        while True:
            choice = input(prompt_text).strip()
            if choice in valid_ai_keys:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between {min_key} and {max_key}")

    def _choose_play_mode(self) -> str:
        """Prompt the user to choose between 1-player and 2-player mode.

        Returns:
            str: 'ai' for single-player, 'human' for two-player.
        """
        while True:
            choice = input("Will this be a 1-player or 2-player game? (Enter 1 or 2): ").strip()
            if choice == "1":
                return "ai"
            elif choice == "2":
                return "human"
            else:
                print("Invalid choice. Please enter either 1 or 2.")

    def get_game_config(self) -> dict[str, str]:
        """Gathers player setup details from user input and returns a configuration dictionary.

        This method collects the name and marker for Player 1, determines whether Player 2 is
        human or AI, and assigns the appropriate name and difficulty key for Player 2.

        Returns:
            dict[str, str]: A dictionary containing:
                - "p1_name": Name of Player 1.
                - "p1_marker": Marker chosen by Player 1 ("X" or "O").
                - "p2_type": Difficulty key for Player 2 ("0" for human, otherwise AI key).
                - "p2_name": Name of Player 2 ("Bot" if AI, otherwise user-provided).
        """
        game_config = {}
        game_config["p1_name"] = self._get_human_name()
        game_config["p1_marker"] = self._choose_marker()

        mode = self._choose_play_mode()

        # "0" is the key for PlayerType.HUMAN
        game_config["p2_type"] = "0" if mode == "human" else self._choose_ai_difficulty()

        game_config["p2_name"] = self._get_human_name() if game_config["p2_type"] == "0" else "Bot"

        return game_config

    def prettify_board(self) -> str:
        """Converts the 2D board structure into a formatted string for display.

        Cells containing None are visually rendered as an empty space (" ").

        Returns:
            str: The multi-line string representation of the board grid.

        Raises:
            ValueError: If the game engine has not been injected.
        """
        if self._game is None:
            raise ValueError("Game engine not set. Call set_engine() before rendering the board.")

        # Flatten the board list for easier indexing in the f-string
        pos = [cell for row in self._game.get_board_state() for cell in row]

        # Use a visual placeholder for None values
        display_pos = [p if p is not None else " " for p in pos]

        pretty_board = dedent(
            f"""\
        -------------
        | {display_pos[0]} | {display_pos[1]} | {display_pos[2]} |
        -------------
        | {display_pos[3]} | {display_pos[4]} | {display_pos[5]} |
        -------------
        | {display_pos[6]} | {display_pos[7]} | {display_pos[8]} |
        -------------
        """
        )
        return pretty_board

    def display_game_state(self) -> None:
        """Prints the current state of the game board to the console.

        Calls prettify_board() to get the formatted string before printing.
        """
        print(self.prettify_board())

    def display_message(self, message: str) -> None:
        """Displays general info for the user.

        Args:
            message: The message string to display.
        """
        print(f"\n{message}")

    def display_error(self, error: str) -> None:
        """Displays warning or error feedback.

        Args:
            error: The error message to display.
        """
        print(f"!!! {error} !!!")

    def display_winner(self, winner_name: str) -> None:
        """Announces the end of the game.

        Args:
            winner_name: The name of the winner, or None if the game is a draw.
        """
        if winner_name:
            print(f"\n*** Game Over! Winner: {winner_name}! ***")
        else:
            print("\n*** Game Over! It's a draw! ***")
