import unittest

from texas_holdem.card import HoleCards
from texas_holdem.shorthand_notations import *
from texas_holdem.find_better_hole_cards import *


class TestFindBetterHoleCards(unittest.TestCase):
  def test_list_remaining_cards(self):
    cards_seen = [S2, S3, S4, S5, S6, S7]
    remaining_cards = list_remaining_cards(cards_seen)
    self.assertEqual(len(remaining_cards), 52 - len(cards_seen))
    # remaining_cards are all distrinct
    self.assertEqual(len(set(remaining_cards)), len(remaining_cards))
    # Check that cards_seen are really not among remaining_cards.
    self.assertEqual(
        len(set(cards_seen + remaining_cards)),
        len(cards_seen) + len(remaining_cards)
    )

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
