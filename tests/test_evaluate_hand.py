import unittest

from texas_holdem.evaluate_hand import *
from texas_holdem.shorthand_notations import *


class TestHandRankSorting(unittest.TestCase):
  def test_sort_hand_ranks_in_incr_order(self):
    sorted_ranks = sort_hand_ranks_in_incr_order()
    self.assertListEqual(
        sorted_ranks,
        [
          HandRank.HIGH_CARD, HandRank.ONE_PAIR, HandRank.TWO_PAIRS, HandRank.THREE_OF_A_KIND,
          HandRank.STRAIGHT, HandRank.FLUSH, HandRank.FULL_HOUSE, HandRank.FOUR_OF_A_KIND,
          HandRank.STRAIGHT_FLUSH, HandRank.ROYAL_FLUSH
        ])

  def test_sort_hand_ranks_in_decr_order(self):
    sorted_ranks = sort_hand_ranks_in_decr_order()
    self.assertListEqual(
        sorted_ranks,
        [
          HandRank.ROYAL_FLUSH, HandRank.STRAIGHT_FLUSH,
          HandRank.FOUR_OF_A_KIND, HandRank.FULL_HOUSE, HandRank.FLUSH, HandRank.STRAIGHT,
          HandRank.THREE_OF_A_KIND, HandRank.TWO_PAIRS,  HandRank.ONE_PAIR, HandRank.HIGH_CARD
        ])


class TestEvaluateHand(unittest.TestCase):
  def test_high_card(self):
    hole_cards = [S2, S3]
    board = [C5, C6, D8, D9, HA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.HIGH_CARD,
        tie_breaker_card_ranks=[Rank.ACE, Rank.NINE, Rank.EIGHT, Rank.SIX, Rank.FIVE]
        )
    self.assertEqual(hand_value, expected)

  def test_one_pair(self):
    hole_cards = [S2, S6]
    board = [C5, C6, D8, D9, HA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.ONE_PAIR,
        tie_breaker_card_ranks=[Rank.SIX, Rank.ACE, Rank.NINE, Rank.EIGHT]
        )
    self.assertEqual(hand_value, expected)

  def test_two_pairs(self):
    hole_cards = [S2, S6]
    board = [C5, C6, D9, H9, HA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.TWO_PAIRS,
        tie_breaker_card_ranks=[Rank.NINE, Rank.SIX, Rank.ACE]
        )
    self.assertEqual(hand_value, expected)

  def test_three_of_a_kind(self):
    hole_cards = [S2, S6]
    board = [C5, C6, D6, H9, HA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.THREE_OF_A_KIND,
        tie_breaker_card_ranks=[Rank.SIX,  Rank.ACE, Rank.NINE]
        )
    self.assertEqual(hand_value, expected)

  def test_straight(self):
    board = [H4, D5, H7, C8, CA]
    # Tests that it doesn't cause problem if the cards not part of the straight are higher ranked
    # (even if they form a 2-long sequence).
    hole_cards1 = [S6, SK]
    # Tests that it doesn't cause problem if one of the cards forming the straight has a pair
    # with one of the cards that don't.
    hole_cards2 = [S6, H6]
    # Tests that if we have a >5 long sequence then we find the subsequence starting with the
    # highest rank.
    hole_cards3 = [S3, S6]

    hand_value1 = get_hand_value(hole_cards1, board)
    hand_value2 = get_hand_value(hole_cards2, board)
    hand_value3 = get_hand_value(hole_cards3, board)
    expected = HandValue(
        rank=HandRank.STRAIGHT,
        tie_breaker_card_ranks=[Rank.EIGHT]
        )
    self.assertEqual(hand_value1, expected)
    self.assertEqual(hand_value2, expected)
    self.assertEqual(hand_value3, expected)

  def test_four_consecutive_ranks_do_not_count_as_straight(self):
    hole_cards = [S2, S3]
    board = [D4, D5, CJ, CQ, HK]
    hand_value = get_hand_value(hole_cards, board)
    self.assertEqual(hand_value.rank, HandRank.HIGH_CARD)

  def test_straight_starting_with_ace(self):
    '''Tests the case where the ACE acts like the rank preceding rank TWO.

    For the purpose of creating a straight hand, ACEs can be considered as either the next card
        after KING or the one before TWO.
    '''
    hole_cards = [S2, SA]
    board = [H3, H4, C5, CQ, DK]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.STRAIGHT,
        tie_breaker_card_ranks=[Rank.FIVE]
        )
    self.assertEqual(hand_value, expected)

  def test_straight_ending_with_ace(self):
    '''Tests the case where the ACE acts like the rank following the rank king.

    For the purpose of creating a straight hand, ACEs can be considered as either the next card
        after KING or the one before TWO.
    '''
    hole_cards = [S2, SA]
    board = [H3, H10, CJ, CQ, DK]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.STRAIGHT,
        tie_breaker_card_ranks=[Rank.ACE]
        )
    self.assertEqual(hand_value, expected)

  def test_flush(self):
    hole_cards = [S2, S4]
    board = [S5, S6, S10, CQ, SK]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.FLUSH,
        tie_breaker_card_ranks=[Rank.KING, Rank.TEN, Rank.SIX, Rank.FIVE, Rank.FOUR]
        )
    self.assertEqual(hand_value, expected)

  def test_full_house_when_triplet_is_higher(self):
    'Tests the case when the triplet of the full house is of higher rank than the pair.'
    hole_cards = [S2, S3]
    board = [C2, D2, D3, SK, SA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.FULL_HOUSE,
        tie_breaker_card_ranks=[Rank.TWO, Rank.THREE])
    self.assertEqual(hand_value, expected)

  def test_full_house_when_pair_is_higher(self):
    'Tests the case when the pair in the full house is of higher rank than the triplet.'
    hole_cards = [S2, S3]
    board = [C2, C3, D3, SK, SA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.FULL_HOUSE,
        tie_breaker_card_ranks=[Rank.THREE, Rank.TWO])
    self.assertEqual(hand_value, expected)

  def test_four_of_a_kind(self):
    hole_cards = [S2, S6]
    board = [C6, C6, D6, HA, HA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.FOUR_OF_A_KIND,
        tie_breaker_card_ranks=[Rank.SIX,  Rank.ACE]
        )
    self.assertEqual(hand_value, expected)

  def test_straight_flush(self):
    hole_cards = [S2, S3]
    board = [S4, S5, S6, S7, DK]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.STRAIGHT_FLUSH,
        tie_breaker_card_ranks=[Rank.SEVEN]
        )
    self.assertEqual(hand_value, expected)

  def test_straight_flush_starting_with_ace(self):
    '''Tests the case where the ACE acts like the rank preceding rank TWO.

    For the purpose of creating a straight flush hand, ACEs can be considered as either the next
    card after KING or the one before TWO.
    '''
    hole_cards = [S2, SA]
    board = [S3, S4, S5, CQ, DK]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.STRAIGHT_FLUSH,
        tie_breaker_card_ranks=[Rank.FIVE]
        )
    self.assertEqual(hand_value, expected)

  def test_royal_flush(self):
    hole_cards = [C2, S10]
    board = [D2, SJ, SQ, SK, SA]
    hand_value = get_hand_value(hole_cards, board)
    expected = HandValue(
        rank=HandRank.ROYAL_FLUSH,
        tie_breaker_card_ranks=[])
    self.assertEqual(hand_value, expected)
