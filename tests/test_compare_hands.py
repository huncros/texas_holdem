import unittest
from itertools import permutations

from texas_holdem.card import HoleCards, Board, Rank
from texas_holdem.evaluate_hand import HandRank, HandValue, get_hand_value
from texas_holdem.compare_hands import has_better_hand_than_hand_value
from texas_holdem.shorthand_notations import *


class TestHasBetterHandThenHandValue(unittest.TestCase):
  'Tests for the function has_better_hand_than_hand_value.'
  def test_works_when_comparing_different_ranks(self):
    'Test cases where we compare a hand to a HandValue with different rank.'
    # We want to check all combinations so for each hand rank we list 7 cards (the number of
    # cards available for each player to form their hand) where the best hand is of the given
    # rank. We compare all possible pairs among them.
    cards_for_ranks = {
        HandRank.HIGH_CARD: [H2, H3, S6, S7, C8, C10, DA],
        HandRank.ONE_PAIR: [H2, H3, S6, S7, C7, C10, DA],
        HandRank.TWO_PAIRS: [H2, H3, S6, C6, S7, C7, DA],
        HandRank.THREE_OF_A_KIND: [H2, H3, S6, C6, D6, S7, DA],
        HandRank.STRAIGHT: [H2, H3, S6, S7, C8, C9, D10],
        HandRank.FLUSH: [H2, H3, S6, S7, S9, SJ, SA],
        HandRank.FULL_HOUSE: [H2, H3, S6, C6, D6, S8, D8],
        HandRank.FOUR_OF_A_KIND: [H2, H3, S6, C6, D6, H6, DA],
        HandRank.STRAIGHT_FLUSH: [H2, H3, S6, S7, S8, S9, S10],
        HandRank.ROYAL_FLUSH: [H2, H3, S10, SJ, SQ, SK, SA],
    }
    # calculate and store the `HandValue`s for the cards for each rank so we can reuse them
    # during the comparisons.
    hand_values = {}
    for rank, cards in cards_for_ranks.items():
      hole_cards = HoleCards(*cards[:2])
      board = Board(*cards[2:])
      hv = get_hand_value(hole_cards, board)
      self.assertEqual( hv.rank, rank, msg=(
            f'Cards {cards} are supposed to form a hand of rank {rank.name} but it is of ' +
            f'{hv.rank.name}.')
          )
      hand_values[rank] = hv
    for r1, r2 in permutations(cards_for_ranks.keys(), 2):
      cards = cards_for_ranks[r1]
      hole_cards = HoleCards(*cards[:2])
      board = Board(*cards[2:])
      compare_to = hand_values[r2]
      is_the_hand_better = has_better_hand_than_hand_value(hole_cards, board, compare_to)
      expected = r1 > r2
      self.assertEqual(is_the_hand_better, expected, msg=(
        f'Comparing whether the cards {cards} contain a better hand than {compare_to} should' +
        f'return: {expected}.'))

  def test_works_when_comparing_same_ranks(self):
    board = [S5, C5, S7, D10, DA]
    hole_cards = [CK, CA]  # Forms TWO_PAIRS with A and 5, with kicker K.

    lower_hand_value = HandValue(
        rank=HandRank.TWO_PAIRS,
        tie_breaker_card_ranks=[Rank.ACE, Rank.FOUR, Rank.ACE])
    equal_hand_value = HandValue(
        rank=HandRank.TWO_PAIRS,
        tie_breaker_card_ranks=[Rank.ACE, Rank.FIVE, Rank.KING])
    stronger_hand_value = HandValue(
        rank=HandRank.TWO_PAIRS,
        tie_breaker_card_ranks=[Rank.ACE, Rank.SIX, Rank.TWO])

    self.assertTrue(has_better_hand_than_hand_value(hole_cards, board, lower_hand_value))
    self.assertFalse(has_better_hand_than_hand_value(hole_cards, board, equal_hand_value))
    self.assertFalse(has_better_hand_than_hand_value(hole_cards, board, stronger_hand_value))
