import unittest
import src.main as main
from textwrap import dedent

class TestNewBoard(unittest.TestCase):

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

    def test_prettify_empty_board(self):
        """Test that prettyify_board function correctly formats the board.
        None values should display a space in that cell"""

        board = main.new_board()
        pretty_board = main.prettify_board(board)

        expected_board = dedent("""\
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
        """)

        self.assertEqual(pretty_board, expected_board)
    
    def test_prettify_full_board(self):
        """Test that prettyify_board function correctly formats a full board."""

        board = [
                 ["X", "O", "O"],
                 ["O", "O", "X"],
                 ["X", "X", "O"]
                ]

        expected_board = dedent("""\
            -------------
            | X | O | O |
            -------------
            | O | O | X |
            -------------
            | X | X | O |
            -------------
        """)

        pretty_board = main.prettify_board(board)
        self.assertEqual(pretty_board, expected_board)

if __name__ == '__main__':
    unittest.main()