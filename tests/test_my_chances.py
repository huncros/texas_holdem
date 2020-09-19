import unittest

from texas_holdem.card import HoleCards
from texas_holdem.my_chances import compute, n_choose_m, Opponent, OpponentError
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

  def test_my_chances_with_assumptions(self):
    'Test the case when we have and assumption about our opponents hand.'

    class RevealedBadCard(Opponent):
      '''The opponent didn't hide their hole cards correctly and so we have seen one of their
      hole cards which is H5.
      '''
      @staticmethod
      def hole_card_weight(hole_cards, board):
        return 1 if H5 in hole_cards else 0

    opp = RevealedBadCard()
    my_chances = compute([DK, CK], [SJ, SQ, SK, HK], against=opp)
    # We have a FOUR_OF_A_KIND so the only way to beat it is to either form STRAIGHT_FLUSH by
    # getting the cards S9, S10 or to form ROYAL_FLUSH by getting the cards S10, SA.
    # We know that the opponent has H5 as his hole card which leaves the following mutually
    # exclusive cases where the opponent would have a better hand than us:
    #   1. The 5th community card is SA. The opponent's second hole card is S10.
    #   2. The 5th community card is S10. The opponent's second hole card is S9 or SA.
    #   3. The 5th community card is S9. The opponent's hole second hole card is S10.
    num_remaining_cards = 52 - 7
    all_possibilities = num_remaining_cards * (num_remaining_cards - 1)
    opponents_chance = (1 + 2 + 1) / all_possibilities
    self.assertEqual(my_chances, 1 - opponents_chance)

  def test_error_when_assuming_negative_weight(self):
    '''Only non-negative weights should be used for assumptions.

    An error should be raised otherwise.
    '''
    class NegativeWeights(Opponent):
      @staticmethod
      def hole_card_weight(hole_cards, board):
        return -1 if hole_cards == HoleCards(S2, S3) else 1

    opp = NegativeWeights()
    with self.assertRaises(OpponentError) as exc:
      my_chances = compute([DK, CK], [SJ, SQ, SK, HK], against=opp)
    self.assertIn('returns negative weights', str(exc.exception))

  def test_error_when_assuming_all_weights_are_zero(self):
    '''At least one weight used for assumptions needs to be positive.

    An error should be raised otherwise.
    '''
    class AllZeros(Opponent):
      @staticmethod
      def hole_card_weight(hole_cards, board):
        return 0

    opp = AllZeros()
    with self.assertRaises(OpponentError) as exc:
      my_chances = compute([DK, CK], [SJ, SQ, SK, HK], against=opp)
    self.assertIn('returns 0 for every possible', str(exc.exception))
