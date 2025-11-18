from textwrap import dedent
from src.core import PlayerType
from src.views.abstract_view import AbstractView


class CLIView(AbstractView):
    """Handles user input and board rendering for a command-line Tic-Tac-Toe game.

    Provides validated input prompts for player setup and AI difficulty selection,
    and renders the game board in a human-readable format."""

    def _get_human_name(self) -> str:
        """Prompt the user to enter their name.
        Keeps asking until a non-empty string is provided.
        Returns:
            str: The user's name."""
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
            str: The chosen marker ('X' or 'O')."""
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
            str: The chosen difficulty level key."""
        MIN_KEY = PlayerType.get_min_difficulty_key()
        MAX_KEY = PlayerType.get_max_difficulty_key()

        valid_ai_keys = []
        prompt = "Choose your opponent's difficulty:\n"
        for key, description in PlayerType.get_ai_options():
            valid_ai_keys.append(key)
            prompt += f"  {key}) {description}\n"
        prompt += f"Enter your choice ({MIN_KEY}-{MAX_KEY}): "

        while True:
            choice = input(prompt).strip()
            if choice in valid_ai_keys:
                return choice
            else:
                print(
                    f"Invalid choice. Please enter a number between {MIN_KEY} and {MAX_KEY}"
                )

    def _choose_play_mode(self) -> str:
        """Prompt the user to choose between 1-player and 2-player mode.

        Returns:
            str: 'ai' for single-player, 'human' for two-player."""
        while True:
            choice = input(
                "Will this be a 1-player or 2-player game? (Enter 1 or 2): "
            ).strip()
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
                - "p2_name": Name of Player 2 ("Bot" if AI, otherwise user-provided)."""
        game_config = {}
        game_config["p1_name"] = self._get_human_name()
        game_config["p1_marker"] = self._choose_marker()
        game_config["p2_type"] = (
            "0" if self._choose_play_mode() == "human" else self._choose_ai_difficulty()
        )
        game_config["p2_name"] = (
            self._get_human_name() if game_config["p2_type"] == "0" else "Bot"
        )
        return game_config

    def prettify_board(self) -> str:
        """Converts the 2D board structure into a formatted string for display.

        Cells containing None are visually rendered as an empty space (" ").

        Returns:
            str: The multi-line string representation of the board grid"""
        if not hasattr(self, "_game"):
            raise ValueError(
                "Game engine not set. Call set_engine() before rendering the board."
            )

        pos = [cell for row in self._game.get_board_state() for cell in row]
        pretty_board = dedent(
            f"""\
        -------------
        | {pos[0] if pos[0] else " "} | {pos[1] if pos[1] else " "} | {pos[2] if pos[2] else " "} |
        -------------
        | {pos[3] if pos[3] else " "} | {pos[4] if pos[4] else " "} | {pos[5] if pos[5] else " "} |
        -------------
        | {pos[6] if pos[6] else " "} | {pos[7] if pos[7] else " "} | {pos[8] if pos[8] else " "} |
        -------------
        """
        )
        return pretty_board

    def display_game_state(self) -> None:
        """Fulfills the AbstractView contract and prints the current state of the game board to the console.

        It calls prettify_board() to get the formatted string before printing."""
        print(self.prettify_board())

    def display_message(self, message: str) -> None:
        """General info for the user"""
        print(f"\n{message}")

    def display_error(self, error: str) -> None:
        """Warning/Error feedback"""
        print(f"!!! {error} !!!")

    def display_winner(self, winner_name: str) -> None:
        """End of game announcement"""
        if winner_name:
            print(f"\n*** Game Over! Winner: {winner_name}! ***")
        else:
            print(f"\n*** Game Over! It's a draw! ***")
