import unittest

from texas_holdem.card import *

class TestCard(unittest.TestCase):
  def test_card_value(self):
    S4 = Card(Suit.SPADES, Rank.FOUR)
    value = card_value(S4)
    self.assertEqual(value, 4)

  def test_card_str(self):
    self.assertEqual(str(Card(suit=Suit.HEARTS, rank=Rank.SIX)), 'H6')
    self.assertEqual(str(Card(suit=Suit.SPADES, rank=Rank.TEN)), 'S10')
    self.assertEqual(str(Card(suit=Suit.CLUBS, rank=Rank.ACE)), 'CA')

  def test_hole_card_comparison(self):
    S2 = Card(suit=Suit.SPADES, rank=Rank.TWO)
    DA = Card(suit=Suit.DIAMONDS, rank=Rank.ACE)
    hc1 = HoleCards(S2, DA)
    hc2 = HoleCards(DA, S2)
    self.assertEqual(hc1, hc2)
