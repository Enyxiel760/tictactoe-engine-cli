import unittest
from src.engine import GameEngine
from src.players.abstract_player import AbstractPlayer


class DummyPlayer(AbstractPlayer):
    """A concrete player class used only for testing the GameEngine.
    It complies with the full AbstractPlayer contract."""

    def get_move(self):
        return (0, 0)


class TestGameEngine(unittest.TestCase):
    """Base class setup for all GameEngine tests."""

    def setUp(self):
        """Set up a fresh GameEngine instance before each test."""
        self.player_x = DummyPlayer("Alice", marker="X")
        self.player_o = DummyPlayer("Fred", marker="O")
        self.game = GameEngine(self.player_x, self.player_o)


class TestNewBoard(TestGameEngine):
    """Tests the GameEngine's board initialization (via _new_board)."""

    def test_initial_board_state(self):
        """Test that the board attribute is a 3x3 grid with all positions set to 'None'"""
        board = self.game.board

        self.assertEqual(len(board), 3)  # Check there are 3 rows

        for row in board:
            self.assertEqual(len(row), 3)  # Check each row has 3 columns

            for cell in row:
                self.assertIsNone(cell)  # Check each cell is None


class TestMakeMove(TestGameEngine):
    """Tests the make_move method for correct symbol placement and mutation."""

    def test_make_move_places_correct_symbol(self):
        """Tests that the current player's marker is placed correctly."""
        move = (0, 0)
        self.game.make_move(move)

        self.assertEqual(self.game.board[0][0], "X")  # First move is always 'X'

        self.game.switch_player()
        move = (1, 1)
        self.game.make_move(move)
        self.assertEqual(self.game.board[1][1], "O")

    def test_make_move_mutates_board(self):
        """Tests that make_move modifies the internal board state (mutation property)"""
        original_board_reference = self.game.board
        self.game.make_move((0, 0))

        self.assertIs(self.game.board, original_board_reference)


class TestGetWinner(TestGameEngine):
    """Tests the get_winner method across all win/non-win conditions."""

    def test_get_winner_empty_board(self):
        """Tests that a brand new, empty board (all None values) is correctly identified as having no
        winner (returns None)."""
        result = self.game.get_winner()
        self.assertIsNone(result)

    def test_get_winner_almost_win(self):
        """Tests a partial board setup containing multiple two-in-a-row patterns to ensure no premature
        winner is declared (returns None)."""
        self.game.board = [["X", "X", None], ["O", "O", None], [None, "X", "O"]]
        result = self.game.get_winner()
        self.assertIsNone(result)

    def test_get_winner_horizontal_win(self):
        """Tests that a horizontal win (three identical, non-None symbols in a row) is correctly detected."""
        self.game.board = [["X", "X", None], ["O", "O", None], ["X", "X", "X"]]
        result = self.game.get_winner()
        self.assertEqual(result, "X")

    def test_get_winner_vertical_win(self):
        """Tests that a vertical win (three identical, non-None symbols in a row) is correctly detected."""
        self.game.board = [["X", "X", None], ["X", "O", None], ["X", "O", "O"]]
        result = self.game.get_winner()
        self.assertEqual(result, "X")

    def test_get_winner_diagonal_win(self):
        """Tests that a diagonal win (three identical, non-None symbols in a row) is correctly detected."""
        self.game.board = [["X", "X", "O"], ["O", "O", None], ["O", "X", "X"]]
        result = self.game.get_winner()
        self.assertEqual(result, "O")


class TestIsBoardFull(TestGameEngine):
    """Tests the is_board_full method for draw conditions."""

    def test_is_board_full_empty(self):
        """Tests that a brand new, empty board is correctly identified as NOT full (False)."""
        result = self.game.is_board_full()
        self.assertFalse(result)

    def test_is_board_full_true(self):
        """Tests that a completely occupied board is correctly identified as full (True)."""
        self.game.board = [["X", "X", "O"], ["O", "O", "X"], ["O", "X", "X"]]
        result = self.game.is_board_full()
        self.assertTrue(result)


class TestIsValidMove(TestGameEngine):
    """Tests the is_valid_move method to ensure it correctly identifies empty and occupied spots."""

    def test_is_valid_move_true(self):
        """Tests that an empty spot (None) is correctly reported as a valid move (True)."""
        result = self.game.is_valid_move((0, 0))
        self.assertTrue(result)

    def test_is_valid_move_false(self):
        """Tests that an occupied spot ('X') is correctly reported as an invalid move (False)."""
        self.game.board[0][0] = "X"
        result = self.game.is_valid_move((0, 0))
        self.assertFalse(result)


class TestGameEngineUtilities(TestGameEngine):
    """Tests the new utility methods added to support the main controller loop."""

    def test_get_current_player(self):
        """Tests that get_current_player returns the correct object. Implicitly tests switch_player."""
        self.assertIs(self.game.get_current_player(), self.player_x)
        self.game.switch_player()
        self.assertIs(self.game.get_current_player(), self.player_o)

    def test_get_winner_name_win(self):
        """Tests that get_winner_name returns the correct player's name (not marker) on a win."""
        self.game.board = [["X", "X", "X"], ["O", None, None], [None, None, "O"]]
        winner_name = self.game.get_winner_name(self.game.get_winner())
        self.assertEqual(winner_name, "Alice")

    def test_get_winner_name_draw(self):
        """Tests that get_winner_name returns None when there is no winner (draw or ongoing)."""
        self.game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        winner_name = self.game.get_winner_name(self.game.get_winner())
        self.assertIsNone(winner_name)

    def test_check_game_status_ongoing(self):
        """Tests that check_game_status returns (False, None) for an ongoing game."""
        self.game.board = [["X", "O", None], [None, None, None], [None, None, None]]
        is_over, winner_marker = self.game.check_game_status()
        self.assertFalse(is_over)
        self.assertIsNone(winner_marker)

    def test_check_game_status_win(self):
        """Tests that check_game_status returns (True, 'X') on a winning board."""
        self.game.board = [["X", "X", "X"], ["O", "O", None], [None, None, None]]
        is_over, winner_marker = self.game.check_game_status()
        self.assertTrue(is_over)
        self.assertEqual(winner_marker, "X")

    def test_check_game_status_draw(self):
        """Tests that check_game_status returns (True, None) on a full, drawn board."""
        self.game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "O"]]
        is_over, winner_marker = self.game.check_game_status()
        self.assertTrue(is_over)
        self.assertIsNone(winner_marker)
