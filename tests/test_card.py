import unittest

from texas_holdem.card import *

class TestCard(unittest.TestCase):
  def test_card_value(self):
    S4 = Card(Suit.SPADES, Rank.FOUR)
    value = card_value(S4)
    self.assertEqual(value, 4)

