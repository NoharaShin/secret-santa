"""Unit tests of the functions of the secret_santa module."""

import os
import unittest
from pathlib import Path

import pandas as pd

import secret_santa
from models.santa_pair import SantaPair

APP_PATH = Path(__file__).resolve().parents[3]


class TestSecretSanta(unittest.TestCase):
    def setUp(self) -> None:
        self.participants = pd.DataFrame({
            "Name": ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donder", "Blitzen"],
            "Team": ['A', 'B', 'B', 'A', 'B', 'A', 'A', 'B']
        })
        self.df_no_header = pd.read_csv(os.path.join(APP_PATH, 'data', 'test_no_header.csv'), header=None)
        self.df_one_column_no_header = pd.read_csv(
            os.path.join(APP_PATH, 'data', 'test_one_column_no_header.csv'), header=None)

    def test_shuffle_simple_mode(self) -> None:
        """Test the giver-receiver attribution when the attribution criterion is the name only."""
        pairs = secret_santa.shuffle(self.participants)
        self.assertIsInstance(pairs, list)
        self.assertEqual(len(pairs), len(self.participants))
        for pair in pairs:
            self.assertIsInstance(pair, SantaPair)
            self.assertNotEqual(pair.giver, pair.receiver)

    def test_shuffle_complex_mode(self) -> None:
        """
        Test the giver-receiver attribution when there are more than 1 attribution criterion.
        The criteria for this tests are the name and the team of the participants (i.e. a gift giver should not be
        on the same team as the receiver).
        """
        pairs = secret_santa.shuffle(self.participants, simple_mode=False)
        self.assertIsInstance(pairs, list)
        self.assertEqual(len(pairs), len(self.participants))
        for pair in pairs:
            self.assertIsInstance(pair, SantaPair)
            self.assertNotEqual(pair.giver, pair.receiver)

    def test_shuffle_complex_mode_wrong_criteria(self):
        """
        Test the giver-receiver attribution when there are more than 1 attribution criterion.
        The criteria for this tests are the name and the team of the participants (i.e. a gift giver should not be
        on the same team as the receiver).
        """
        # Value of criteria is negative
        # 1. Test that ValueError is raised as expected
        with self.assertRaises(ValueError):
            secret_santa.shuffle(self.participants, simple_mode=False, criteria=-1)
        # 2. Test that error message is the expected one
        try:
            secret_santa.shuffle(self.participants, simple_mode=False, criteria=-1)
        except ValueError as error:
            self.assertEqual(
                str(error),
                "Wrong value for argument `criteria`: expected positive number lower or equal to 5, got -1 instead.")

        # Value of criteria is higher than 5
        # 1. Test that ValueError is raised as expected
        with self.assertRaises(ValueError):
            secret_santa.shuffle(self.participants, simple_mode=False, criteria=6)
        # 2. Test that error message is the expected one
        try:
            secret_santa.shuffle(self.participants, simple_mode=False, criteria=6)
        except ValueError as error:
            self.assertEqual(
                str(error),
                "Wrong value for argument `criteria`: expected positive number lower or equal to 5, got 6 instead.")

    def test__rename_columns(self):
        """Test if the function _rename_columns() renames the header of the input DataFrame as expected."""
        test_df = secret_santa._rename_columns(self.participants)
        self.assertIsInstance(test_df, pd.DataFrame)
        self.assertEqual(test_df.columns.tolist(), ["name", "criterion-1"])

    def test__add_columns(self):
        """Test if the function _rename_columns() adds the expected header if a CSV with no header is loaded."""
        test_df = secret_santa._rename_columns(self.df_no_header)
        self.assertIsInstance(test_df, pd.DataFrame)
        self.assertEqual(test_df.columns.tolist(), ["name", "criterion-1", "criterion-2"])

    def test__add_single_column(self):
        """Test if the function _rename_columns() adds a header "name" if a CSV of 1 column and no header is loaded."""
        test_df = secret_santa._rename_columns(self.df_one_column_no_header)
        self.assertIsInstance(test_df, pd.DataFrame)
        self.assertEqual(test_df.columns.tolist(), ["name"])


if __name__ == "__main__":
    unittest.main()
