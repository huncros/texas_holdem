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

  def test_parse(self):
    self.assertEqual(parse('S2'), Card(suit=Suit.SPADES, rank=Rank.TWO))
    self.assertEqual(parse('DJ'), Card(suit=Suit.DIAMONDS, rank=Rank.JACK))
    self.assertEqual(parse('CQ'), Card(suit=Suit.CLUBS, rank=Rank.QUEEN))
    self.assertEqual(parse('HK'), Card(suit=Suit.HEARTS, rank=Rank.KING))
    self.assertEqual(parse('SA'), Card(suit=Suit.SPADES, rank=Rank.ACE))
