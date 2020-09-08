import unittest
import operator
from functools import reduce

from texas_holdem.my_chances import compute, n_choose_m
from texas_holdem.shorthand_notations import *


class TestMyChances(unittest.TestCase):
  def test_n_choose_m(self):
    self.assertEqual(n_choose_m(7, 3), 35)

  def test_my_chances(self):
    my_chances = compute([DK, CK], [SJ, SQ, SK, HK])
    # We have a FOUR_OF_A_KIND so the only way to beat it is to either form STRAIGHT_FLUSH by
    # getting the cards S9, S10 or to form ROYAL_FLUSH by getting the cards S10, SA.
    # Our opponent can get these cards either as their hole cards or one of them as the fifth
    # community card.
    # This means that we have the following mutually exlusive cases:
    #   1. The 5th community card is SA. The opponent's hole cards contain S10.
    #   2. The 5th community card is S10. The opponent's hole cards contain at least one card
    #      from (S9, SA).
    #   3. The 5th community card is S9. The opponent's hole cards contain S10.
    #   4. The 5th community card is neither S9, S10 or SA. The opponent's hole cards are either
    #      S9, S10 or S10, SA.
    num_remaining_cards = 52 - 6
    all_possibilities = n_choose_m(num_remaining_cards, 2) * (num_remaining_cards - 2)
    opponents_chance = (
        (num_remaining_cards - 2) +
        (num_remaining_cards - 2) * 2 - 1 +
        (num_remaining_cards - 2) +
        (num_remaining_cards - 3) * 2) / all_possibilities
    self.assertEqual(my_chances, 1 - opponents_chance)

