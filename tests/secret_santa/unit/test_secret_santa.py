"""Unit tests of the functions of the secret_santa module."""

import os
import unittest
from pathlib import Path

import pandas as pd

import secret_santa

APP_PATH = Path(__file__).resolve().parents[3]


class TestSecretSanta(unittest.TestCase):
    def setUp(self):
        self.participants = pd.DataFrame({
            "Name": ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donder", "Blitzen"],
            "Team": ['A', 'B', 'B', 'A', 'B', 'A', 'A', 'B']
        })
        self.df_no_header = pd.read_csv(os.path.join(APP_PATH, 'data', 'test_no_header.csv'), header=None)
        self.df_one_column_no_header = pd.read_csv(
            os.path.join(APP_PATH, 'data', 'test_one_column_no_header.csv'), header=None)

    # def test_shuffle_simple_mode(self):
    #     givers, receivers = secret_santa.shuffle(self.participants)
    #
    # def test_shuffle_complex_mode(self):
    #     givers, receivers = secret_santa.shuffle(self.participants, simple_mode=False)
    #
    # def test_shuffle_complex_mode_wrong_criteria(self):
    #     givers, receivers = secret_santa.shuffle(self.participants, simple_mode=False, criteria=-1)
    #     givers, receivers = secret_santa.shuffle(self.participants, simple_mode=False, criteria=6)

    def test__rename_columns(self):
        """Test if the function _rename_columns() renames the header of the input DataFrame as expected."""
        test_df = secret_santa._rename_columns(self.participants)
        self.assertEqual(test_df.columns.tolist(), ["name", "criterion-1"])

    def test__add_columns(self):
        """Test if the function _rename_columns() adds the expected header if a CSV with no header is loaded."""
        test_df = secret_santa._rename_columns(self.df_no_header)
        self.assertEqual(test_df.columns.tolist(), ["name", "criterion-1", "criterion-2"])

    def test__add_single_column(self):
        """Test if the function _rename_columns() adds a header "name" if a CSV of 1 column and no header is loaded."""
        test_df = secret_santa._rename_columns(self.df_one_column_no_header)
        self.assertEqual(test_df.columns.tolist(), ["name"])


if __name__ == "__main__":
    unittest.main()
