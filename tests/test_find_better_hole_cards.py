import unittest

from texas_holdem.card import HoleCards, Board
from texas_holdem.shorthand_notations import *
from texas_holdem.find_better_hole_cards import find_better_hole_cards


class TestFindBetterHoleCards(unittest.TestCase):
  def test_find_better_hole_cards(self):
    board = Board(H5, C5, SJ, SQ, SK)
    my_hole_cards = HoleCards(HQ, CQ)  # Has FULL_HOUSE with triplet of rank Q and pair of rank 5.
    better_hole_cards = find_better_hole_cards(my_hole_cards, board)

    expected = [
        # Form better FULL_HOUSE with triplet of rank K.
        HoleCards(HK, CK), HoleCards(HK, DK), HoleCards(CK, DK),
        # Form FOUR_OF_A_KIND with rank of 5.
        HoleCards(S5, D5),
        # Form STRAIGHT_FLUSH with highest ranked card being K.
        HoleCards(S9, S10),
        # Form ROYAL_FLUSH.
        HoleCards(S10, SA)
        ]
    self.assertEqual(len(better_hole_cards), len(expected))
    for hc in better_hole_cards:
      self.assertIn(hc, expected)
