'''Computes the rank and relative strength within the rank of the best hand that the player can
form from their 2 hole cards and the 5 community cards (the board).
'''
from enum import IntEnum
from collections import Counter
from typing import List, NamedTuple, Optional

from texas_holdem.card import Card, Rank, card_value, HoleCards, Board


class HandRank(IntEnum):
  HIGH_CARD = 1
  ONE_PAIR = 2
  TWO_PAIRS = 3
  THREE_OF_A_KIND = 4
  STRAIGHT = 5
  FLUSH = 6
  FULL_HOUSE = 7
  FOUR_OF_A_KIND = 8
  STRAIGHT_FLUSH = 9
  ROYAL_FLUSH = 10


def sort_hand_ranks_in_incr_order() -> List[HandRank]:
  return sorted(HandRank)


def sort_hand_ranks_in_decr_order() -> List[HandRank]:
  return sorted(HandRank, reverse=True)


class HandValue(NamedTuple):
  '''Describes the strength of a hand so we can compare hands.

  A hand's strength is primarily determined by its rank (e.g. flush). In the case when two
  hands have the same rank, then which hand is stronger is decided through comparing the rank of
  the cards making up the hand in a decreasing order.
  E.g. if both players have two pairs, then first they compare the rank of their higher ranked
  pair and the higher rank wins. If it's the same, then they compare the rank of their lower
  ranked pair. If it's still equal then they compare the rank of their 5th card which is not
  part of a pair.
  '''
  rank: HandRank
  tie_breaker_card_ranks: List[Rank]


def get_hand_value(hole_cards: HoleCards, board: Board):
  cards = hole_cards + board
  # A hand can satisfy the conditions for multiple ranks (i.e. a 4 of a kind also contains a pair)
  # but we are only interested in the highest rank. So we check the possible ranks starting from the
  # highest one.
  for rank in sort_hand_ranks_in_decr_order():
    check_for_rank = getattr(HandValueWhenRankIsFixedAs, rank.name)
    hand_value = check_for_rank(cards)
    if hand_value is not None:
      return hand_value


class HandValueWhenRankIsFixedAs:
  '''Contains a static method for each hand rank. Each of them take the 7 cards on the table (hole
  cards and the board) as input and looks for the hand that has the highest value as that rank.
  (See the example below if this explanation is not clear).

  If such a hand is found then it returns a HandRank that indicates the strength of the hand as the
  given rank.
  If no hand can be formed with the given rank then the return value is None.

  Example
  -------
  Let's say that the community cards and the player's hole cards are respectively

      S4, S8, D4, D9, C10  |  H9 HK

  Then the hand with the highest rank as a HIGH_CARD is [S8, D9, h9, C10, HK] and the corresponding
  return value would be

      HandValue(rank=HIGH_CARD, tie_breaker_card_ranks=[KING, TEN, NINE, NINE, EIGHT]).

  Note that the chosen hand actually also contains a pair, so we could assign a higher ranked
  `HandValue` but we are only interested in the value of the hand as a HIGH_CARD.

  The same hand would be the highest ranked as ONE_PAIR but the corresponding return value now would
  be

      HandValue(rank=ONE_PAIR, tie_breaker_card_ranks=[NINE, KING, TEN, EIGHT]).
  '''
  @staticmethod
  def ROYAL_FLUSH(cards: List[Card]):
    str_flush_value = HandValueWhenRankIsFixedAs.STRAIGHT_FLUSH(cards)
    if str_flush_value is not None and str_flush_value.tie_breaker_card_ranks == [ Rank.ACE]:
      return HandValue(rank=HandRank.ROYAL_FLUSH, tie_breaker_card_ranks=[])

  @staticmethod
  def STRAIGHT_FLUSH(cards: List[Card]):
    cards_with_most_common_suit = _filter_most_freq_suit(cards)
    if len(cards_with_most_common_suit) < 5:
      return
    straight = _find_highest_ranked_straight(cards_with_most_common_suit)
    if straight is not None:
      return HandValue(rank=HandRank.STRAIGHT_FLUSH, tie_breaker_card_ranks=[straight[0].rank])

  @staticmethod
  def FOUR_OF_A_KIND(cards: List[Card]):
    four_of_a_kind = _find_highest_ranked_n_cards_with_same_rank(cards, n=4)
    if four_of_a_kind is not None:
      kicker = max([c for c in cards if c not in four_of_a_kind], key=card_value)
      tie_breaker_card_ranks = [four_of_a_kind[0].rank] + [kicker.rank]
      return HandValue(
        rank=HandRank.FOUR_OF_A_KIND, tie_breaker_card_ranks=tie_breaker_card_ranks)

  @staticmethod
  def FULL_HOUSE(cards: List[Card]):
    triplet = _find_highest_ranked_n_cards_with_same_rank(cards, n=3)
    if triplet is None:
      return
    remaining_cards = [c for c in cards if c not in triplet]
    pair = _find_highest_ranked_n_cards_with_same_rank(remaining_cards, n=2)
    if pair is None:
      return
    return HandValue(
        rank=HandRank.FULL_HOUSE,
        tie_breaker_card_ranks=[triplet[0].rank, pair[0].rank])

  @staticmethod
  def FLUSH(cards: List[Card]):
    cards_with_most_common_suit = _filter_most_freq_suit(cards)
    if len(cards_with_most_common_suit) >= 5:
      hand = sorted(cards_with_most_common_suit, key=card_value, reverse=True)[:5]
      return HandValue(
          rank=HandRank.FLUSH, tie_breaker_card_ranks=[c.rank for c in hand])

  @staticmethod
  def STRAIGHT(cards: List[Card]):
    straight = _find_highest_ranked_straight(cards)
    if straight is not None:
      return HandValue( rank=HandRank.STRAIGHT, tie_breaker_card_ranks=[straight[0].rank])

  @staticmethod
  def THREE_OF_A_KIND(cards: List[Card]):
    triplet = _find_highest_ranked_n_cards_with_same_rank(cards, n=3)
    if triplet is not None:
      cards_in_decr_order = sorted(cards, key=card_value, reverse=True)
      kicker_card_ranks = [c.rank for c in cards_in_decr_order if c not in triplet][:2]
      tie_breaker_card_ranks = [triplet[0].rank] + kicker_card_ranks
      return HandValue(
        rank=HandRank.THREE_OF_A_KIND, tie_breaker_card_ranks=tie_breaker_card_ranks)

  @staticmethod
  def TWO_PAIRS(cards: List[Card]):
    cards_in_decr_order = sorted(cards, key=card_value, reverse=True)
    neighbors = zip(cards_in_decr_order, cards_in_decr_order[1:])
    pairs = []
    while True:
      try:
        ns = next(neighbors)
        if ns[0].rank == ns[1].rank:
          pairs.append(ns)
          if len(pairs) == 2:
            kicker = next(c for c in cards_in_decr_order if c not in pairs[0] + pairs[1])
            tie_breaker_card_ranks=[p[0].rank for p in pairs] + [kicker.rank]
            return HandValue(rank=HandRank.TWO_PAIRS, tie_breaker_card_ranks=tie_breaker_card_ranks)
          else:
            next(neighbors)
      except StopIteration:
        return

  @staticmethod
  def ONE_PAIR(cards: List[Card]):
    pair = _find_highest_ranked_n_cards_with_same_rank(cards, n=2)
    if pair is not None:
      cards_in_decr_order = sorted(cards, key=card_value, reverse=True)
      kicker_card_ranks = [c.rank for c in cards_in_decr_order if c not in pair][:3]
      tie_breaker_card_ranks = [pair[0].rank] + kicker_card_ranks
      return HandValue(rank=HandRank.ONE_PAIR, tie_breaker_card_ranks=tie_breaker_card_ranks)

  @staticmethod
  def HIGH_CARD(cards: List[Card]):
    card_ranks_in_decr_order = sorted([c.rank for c in cards], reverse=True)
    return HandValue(rank=HandRank.HIGH_CARD, tie_breaker_card_ranks=card_ranks_in_decr_order[:5])


### Utility functions ###


def _find_highest_ranked_straight(cards: List[Card]):
  '''If the input cards contain 5 consecutively ranked cards then it returns the highest ranked such
  5 card.
  Otherwise returns None.
  '''
  cards_in_decr_order = sorted(cards, key=card_value, reverse=True)
  # if Rank.ACE in card_ranks_in_decr_order and Rank.KING in card_ranks_in_decr_order:
  if cards_in_decr_order[0].rank == Rank.ACE:
    # For the purpose of creating a straight, ACEs can be counted as both the rank following KING
    # or preceding rank TWO.
    # We solve this problem by introducing a virtual rank: ACE_LOW, which represents the ACE
    # counted as rank ONE while the original ACE represents the rank following the rank KING.
    # If the cards contain an ACE, we also add an ACE_LOW to consider both possibilities. Since
    # a straight can only contain one ACE, this won't create new straights not originally
    # contained in the cards.
    low_ace = Card(suit=cards_in_decr_order[0].suit, rank=Rank.ACE_LOW)
    cards_in_decr_order.append(low_ace)
  curr_seq = cards_in_decr_order[:1]
  for card in cards_in_decr_order:
    if card.rank == curr_seq[-1].rank:
      continue
    elif card.rank == curr_seq[-1].rank - 1:
      curr_seq.append(card)
      if len(curr_seq) == 5:
        return curr_seq
    else:
      curr_seq = [card]


def _find_highest_ranked_n_cards_with_same_rank(cards: List[Card], n: int):
  '''Among the possible subsets of n cards with same rank, it finds one where this rank is the
  highest possible.

  If there are no n cards with the same rank among the input cards then return None.
  '''
  cards_in_decr_order = sorted(cards, key=card_value, reverse=True)
  slices = zip(*[cards_in_decr_order[i:] for i in range(n)])
  for sl in slices:
    if sl[0].rank == sl[-1].rank:
      return sl

def _filter_most_freq_suit(cards: List[Card]) -> List[Card]:
  'Returns the list of cards that have the most frequent suit among the input cards.'
  num_cards_per_suit = Counter(c.suit for c in cards)
  most_common_suit, num_cards = num_cards_per_suit.most_common(1)[0]
  return [c for c in cards if c.suit == most_common_suit]

