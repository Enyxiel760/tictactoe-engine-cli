"""Player factory for Tic Tac Toe.

Provides a helper function to instantiate player objects based on setup configuration data supplied
by the view layer.
"""

from src import players as p
from src.core import PlayerType


def get_player_instances(setup_data: dict[str, str]) -> tuple[p.AbstractPlayer, p.AbstractPlayer]:
    """Instantiate two player objects based on setup configuration.

    Expects a dictionary structured by the view layer, containing player names, markers, and a
    difficulty key. Assumes the view has validated and formatted this data appropriately.

    Args:
        setup_data: Dictionary containing:
            - "p1_name": Name of player 1.
            - "p1_marker": Marker for player 1 ("X" or "O").
            - "p2_name": Name of player 2.
            - "p2_type": Difficulty key for player 2 ("0" for human, otherwise AI).

    Returns:
        tuple[AbstractPlayer, AbstractPlayer]: Ordered pair of players, with the "X" marker player
            first.
    """
    p2_marker = "X" if setup_data["p1_marker"] == "O" else "O"
    player1 = p.HumanPlayer(setup_data["p1_name"], setup_data["p1_marker"])

    if setup_data["p2_type"] == PlayerType.HUMAN.key:
        player2 = p.HumanPlayer(setup_data["p2_name"], p2_marker)
    else:
        # Dynamically retrieve the specific AI class (e.g., MinimaxAIPlayer)
        ai_class = PlayerType.get_player_class_by_key(setup_data["p2_type"])
        player2 = ai_class(setup_data["p2_name"], p2_marker)

    # Return players in (X, O) order for the engine to initialize correctly
    if player1.marker == "X":
        return player1, player2
    else:
        return player2, player1
