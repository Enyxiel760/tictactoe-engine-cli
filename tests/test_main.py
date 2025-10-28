import unittest
import src.main as main

class TestTicTacToe(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()