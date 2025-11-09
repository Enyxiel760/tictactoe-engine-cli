AI_DIFFICULTIES = {
    "1": "Easy (Random)",
    "2": "Medium (Checks for wins)",
    "3": "Hard (Checks for wins and blocks)",
    "4": "Impossible (Perfect play)",
}
MIN_DIFFICULTY = min(map(int, AI_DIFFICULTIES))
MAX_DIFFICULTY = max(map(int, AI_DIFFICULTIES))


class Menu:
    """Handles user input for game setup, including player name, marker choice, and AI difficulty level.
    All methods are static and return validated user input."""

    @staticmethod
    def get_human_name() -> str:
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

    @staticmethod
    def choose_marker() -> str:
        """Ask the user to choose a marker: 'X' or 'O'.
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

    @staticmethod
    def choose_ai_difficulty() -> str:
        """Display a list of AI difficulty levels and prompt the user to choose one.
        Validates input against the keys in AI_DIFFICULTIES.
        Returns:
            str: The chosen difficulty level key."""
        prompt = "Choose your opponent's difficulty:\n"
        for key, name in AI_DIFFICULTIES.items():
            prompt += f"  {key}) {name}\n"
        prompt += f"Enter your choice ({MIN_DIFFICULTY}-{MAX_DIFFICULTY}): "

        while True:
            choice = input(prompt).strip()
            if choice in AI_DIFFICULTIES:
                return choice
            else:
                print(
                    f"Invalid choice. Please enter a number between {MIN_DIFFICULTY} and {MAX_DIFFICULTY}"
                )
