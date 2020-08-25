import unittest

from texas_holdem.shorthand_notations import *
from texas_holdem.card import Card, Rank, Suit


class TestShorthandNotations(unittest.TestCase):
  def test_cards_are_available_with_their_shorthand_notation(self):
    self.assertEqual(S2, Card(suit=Suit.SPADES, rank=Rank.TWO))
    self.assertEqual(D3, Card(suit=Suit.DIAMONDS, rank=Rank.THREE))
    self.assertEqual(H4, Card(suit=Suit.HEARTS, rank=Rank.FOUR))
    self.assertEqual(C5, Card(suit=Suit.CLUBS, rank=Rank.FIVE))
    self.assertEqual(S6, Card(suit=Suit.SPADES, rank=Rank.SIX))
    self.assertEqual(D7, Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN))
    self.assertEqual(H8, Card(suit=Suit.HEARTS, rank=Rank.EIGHT))
    self.assertEqual(C9, Card(suit=Suit.CLUBS, rank=Rank.NINE))
    self.assertEqual(S10, Card(suit=Suit.SPADES, rank=Rank.TEN))
    self.assertEqual(DJ, Card(suit=Suit.DIAMONDS, rank=Rank.JACK))
    self.assertEqual(HQ, Card(suit=Suit.HEARTS, rank=Rank.QUEEN))
    self.assertEqual(CK, Card(suit=Suit.CLUBS, rank=Rank.KING))
    self.assertEqual(SA, Card(suit=Suit.SPADES, rank=Rank.ACE))
