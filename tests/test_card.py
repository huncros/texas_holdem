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

  def test_list_all_cards(self):
    cards = list(list_all_cards())
    self.assertEqual(len(cards), 52)
    # Check that cards are all distinct.
    self.assertEqual(len(set(cards)), len(cards))
    # Check that we have 4 cards of each existing rank and 0 for ACE_LOW.
    for r in Rank:
      cards_with_rank = [c for c in cards if c.rank == r]
      if r == Rank.ACE_LOW:
        self.assertEqual(len(cards_with_rank), 0)
      else:
        self.assertEqual(len(cards_with_rank), 4)

  def test_list_remaining_cards(self):
    cards_seen = [
        Card(suit=Suit.SPADES, rank=Rank.TWO),
        Card(suit=Suit.SPADES, rank=Rank.THREE),
        Card(suit=Suit.SPADES, rank=Rank.FOUR),
        Card(suit=Suit.SPADES, rank=Rank.FIVE),
        Card(suit=Suit.SPADES, rank=Rank.SIX),
        Card(suit=Suit.SPADES, rank=Rank.SEVEN),
    ]
    remaining_cards = list_remaining_cards(cards_seen)
    self.assertEqual(len(remaining_cards), 52 - len(cards_seen))
    # Check that remaining_cards are all distinct.
    self.assertEqual(len(set(remaining_cards)), len(remaining_cards))
    # Check that cards_seen are really not among remaining_cards.
    self.assertEqual(
        len(set(cards_seen + remaining_cards)),
        len(cards_seen) + len(remaining_cards)
    )

  def test_hole_card_comparison(self):
    S2 = Card(suit=Suit.SPADES, rank=Rank.TWO)
    DA = Card(suit=Suit.DIAMONDS, rank=Rank.ACE)
    hc1 = HoleCards(S2, DA)
    hc2 = HoleCards(DA, S2)
    self.assertEqual(hc1, hc2)
    self.assertSetEqual({hc1}, {hc2})


  def test_parse(self):
    self.assertEqual(parse('S2'), Card(suit=Suit.SPADES, rank=Rank.TWO))
    self.assertEqual(parse('DJ'), Card(suit=Suit.DIAMONDS, rank=Rank.JACK))
    self.assertEqual(parse('CQ'), Card(suit=Suit.CLUBS, rank=Rank.QUEEN))
    self.assertEqual(parse('HK'), Card(suit=Suit.HEARTS, rank=Rank.KING))
    self.assertEqual(parse('SA'), Card(suit=Suit.SPADES, rank=Rank.ACE))
