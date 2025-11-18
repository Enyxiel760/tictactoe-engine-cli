from src.engine import GameEngine
from src import UI, players
from src.core.player_factory import get_player_instances


def main():
    # --- Initialization ---

    # 1. Instantiate the View
    view = UI.CLIView()

    # 2. Get configuration data from the View.
    try:
        setup_data = view.get_game_config()
    except Exception as e:
        print(f"\nFATAL ERROR: Failed to get game configuration. Error: {e}")
        return  # Graceful exit

    # 3. Use the Factory to create player instances
    try:
        player_x, player_o = get_player_instances(setup_data)
    except Exception as e:
        print(f"\nFATAL ERROR: Failed to create players from config. Error: {e}")
        return  # Graceful exit

    # 4. Instantiate Engine
    engine_instance = GameEngine(player_x, player_o)

    # 5. Inject dependencies
    view.set_engine(engine_instance)
    for player in (player_x, player_o):
        if not isinstance(player, players.HumanPlayer):
            player.set_engine(engine_instance)

    # --- Game Loop ---
    print("\n--- Game Starting! ---\n")

    while True:
        # 1. Check game Status
        is_over, winner_marker = engine_instance.check_game_status()
        if is_over:
            break  # Exit loop if game is terminated

        current_player = engine_instance.get_current_player()

        # 2. Display state
        print(f"\n--- It's {current_player.name}'s turn ({current_player.marker}). ---")
        view.display_game_state()

        # 3. Carry out turn
        move = current_player.get_move()
        while not engine_instance.is_valid_move(move):
            print("Invalid move. Can only place marker on empty spots.")
            move = current_player.get_move()
        engine_instance.make_move(move)
        engine_instance.switch_player()

    # --- Game End ---

    # 1. Render final board
    view.display_game_state()

    # 2. Determine and translate winner
    winner_name = engine_instance.get_winner_name(winner_marker)

    # 3. Display final result
    if winner_name is not None:
        print(f"\nGame Over! Winner: {winner_name}!")
    else:
        print("\nGame Over! It's a draw!")


if __name__ == "__main__":
    main()
