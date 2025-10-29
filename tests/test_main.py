import unittest
from unittest.mock import patch
import src.main as main
from textwrap import dedent


class TestNewBoard(unittest.TestCase):
    """Tests the new_board function and its initial state."""

    def test_new_board(self):
        """Test that the new_board function creates an empty board correctly.
        Should be a 3x3 grid with all positions set to None.
        """
        board = main.new_board()

        self.assertEqual(len(board), 3)  # Check there are 3 rows

        for row in board:
            self.assertEqual(len(row), 3)  # Check each row has 3 columns

            for cell in row:
                self.assertIsNone(cell)  # Check each cell is None


class TestPrettifyBoard(unittest.TestCase):
    """Tests the prettify_board function's formatting on empty and fully occupied boards."""

    def test_prettify_empty_board(self):
        """Test that an empty board is formatted correctly, converting all None values to spaces (' ')."""
        board = main.new_board()
        pretty_board = main.prettify_board(board)

        expected_board = dedent(
            """\
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
        """
        )
        self.assertEqual(pretty_board, expected_board)

    def test_prettify_full_board(self):
        """Tests that a fully occupied board with 'X' and 'O' symbols is formatted correctly."""
        board = [["X", "O", "O"], ["O", "O", "X"], ["X", "X", "O"]]

        expected_board = dedent(
            """\
            -------------
            | X | O | O |
            -------------
            | O | O | X |
            -------------
            | X | X | O |
            -------------
        """
        )
        pretty_board = main.prettify_board(board)
        self.assertEqual(pretty_board, expected_board)


@patch("src.main.input")
class TestGetMove(unittest.TestCase):
    """Tests the get_move function's input validation (numeric and range) and coordinate conversion."""

    def test_get_move_non_numeric(self, mock_input):
        """Tests that the function handles non-numeric input ('hello') by looping once and then
        accepting the valid input '5'."""
        mock_input.side_effect = ["hello", "5"]
        result = main.get_move()
        self.assertEqual(result, (1, 1))

    def test_get_move_valid_input(self, mock_input):
        """Tests the base case of receiving a single, valid numeric input ('8') and verifying the correct
        coordinates (2, 1)."""
        mock_input.return_value = "8"
        result = main.get_move()
        self.assertEqual(result, (2, 1))

    def test_get_move_low_boundary(self, mock_input):
        """Tests the low boundary condition by rejecting '0' and then accepting the valid input '1'."""
        mock_input.side_effect = ["0", "1"]
        result = main.get_move()
        self.assertEqual(result, (0, 0))

    def test_get_move_high_boundary(self, mock_input):
        """Tests the high boundary condition by rejecting '10' and then accepting the valid input '9'."""
        mock_input.side_effect = ["10", "9"]
        result = main.get_move()
        self.assertEqual(result, (2, 2))


class TestMakeMove(unittest.TestCase):
    """Tests the make_move function to ensure immutability and correct symbol placement."""

    def test_make_move(self):
        """Tests that a move is placed correctly and that the original board is not mutated"""
        board = main.new_board()
        new_board = main.make_move("X", (0, 0), board)
        self.assertEqual(new_board[0][0], "X")
        self.assertIsNone(board[0][0])


class TestGetWinner(unittest.TestCase):
    """Tests the get_winner function across all win/non-win conditions."""

    def test_get_winner_empty_board(self):
        """Tests that a brand new, empty board (all None values) is correctly identified as having no
        winner (returns None)."""
        board = main.new_board()
        result = main.get_winner(board)
        self.assertIsNone(result)

    def test_get_winner_almost_win(self):
        """Tests a partial board setup containing multiple two-in-a-row patterns to ensure no premature
        winner is declared (returns None)."""
        board = [["X", "X", None], ["O", "O", None], [None, "X", "O"]]
        result = main.get_winner(board)
        self.assertIsNone(result)

    def test_get_winner_horizontal_win(self):
        """Tests that a horizontal win (three identical, non-None symbols in a row) is correctly detected."""
        board = [["X", "X", None], ["O", "O", None], ["X", "X", "X"]]
        result = main.get_winner(board)
        self.assertEqual(result, "X")

    def test_get_winner_vertical_win(self):
        """Tests that a vertical win (three identical, non-None symbols in a row) is correctly detected."""
        board = [["X", "X", None], ["X", "O", None], ["X", "O", "O"]]
        result = main.get_winner(board)
        self.assertEqual(result, "X")

    def test_get_winner_diagonal_win(self):
        """Tests that a diagonal win (three identical, non-None symbols in a row) is correctly detected."""
        board = [["X", "X", "O"], ["O", "O", None], ["O", "X", "X"]]
        result = main.get_winner(board)
        self.assertEqual(result, "O")


class TestIsBoardFull(unittest.TestCase):
    """Tests the is_board_full function for draw conditions."""

    def test_is_board_full_empty(self):
        """Tests that a brand new, empty board is correctly identified as NOT full (False)."""
        board = main.new_board()
        result = main.is_board_full(board)
        self.assertFalse(result)

    def test_is_board_full_true(self):
        """Tests that a completely occupied board is correctly identified as full (True)."""
        board = [["X", "X", "O"], ["O", "O", "X"], ["O", "X", "X"]]
        result = main.is_board_full(board)
        self.assertTrue(result)


class TestIsValidMove(unittest.TestCase):
    """Tests the is_valid_move function to ensure it correctly identifies empty and occupied spots."""

    def test_is_valid_move_true(self):
        """Tests that an empty spot (None) is correctly reported as a valid move (True)."""
        board = main.new_board()
        result = main.is_valid_move((0, 0), board)
        self.assertTrue(result)

    def test_is_valid_move_false(self):
        """Tests that an occupied spot ('X') is correctly reported as an invalid move (False)."""
        board = main.new_board()
        board[0][0] = "X"
        result = main.is_valid_move((0, 0), board)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
