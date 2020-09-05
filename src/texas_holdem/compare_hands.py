'Compares your hand with those of your opponents.'
from texas_holdem.card import HoleCards, Board
from texas_holdem.evaluate_hand import sort_hand_ranks_in_incr_order, HandRank, HandValue, \
    HandValueWhenRankIsFixedAs

# Some hand ranks' criteria also includes the criteria for weaker hand ranks.
# E.g. a FOUR_OF_A_KIND also satisfies the criteria for TWO_PAIRS, only with the the pairs being
# of the same rank.
# As a consequence, if we had checked that cards available to the player don't contain TWO_PAIRS
# then we also know that they don't contain FOUR_OF_A_KIND (or with the same logic: FULL_HOUSE)
# either. This can be used to decrease the computation needed when comparing hands.
_STRICTER_VERSIONS_OF_HAND_RANKS = {
    HandRank.ONE_PAIR: [
      HandRank.TWO_PAIRS, HandRank.THREE_OF_A_KIND, HandRank.FULL_HOUSE, HandRank.FOUR_OF_A_KIND
      ],
    HandRank.TWO_PAIRS: [HandRank.FULL_HOUSE, HandRank.FOUR_OF_A_KIND],
    HandRank.THREE_OF_A_KIND: [HandRank.FULL_HOUSE, HandRank.FOUR_OF_A_KIND],
    HandRank.STRAIGHT: [HandRank.STRAIGHT_FLUSH, HandRank.ROYAL_FLUSH],
    HandRank.FLUSH: [HandRank.STRAIGHT_FLUSH, HandRank.ROYAL_FLUSH],
    HandRank.STRAIGHT_FLUSH: [HandRank.ROYAL_FLUSH],
}

def has_better_hand_than_hand_value(
    hole_cards: HoleCards, board: Board, compare_to: HandValue) -> bool:
  '''Takes a `HandValue` object and checks whether a better hand can be formed from the 7 cards
  available to the player.

  By using a `HandValue` object for the comparison instead of a set of cards makes it cheaper
  to compare a hand against the hands of multiple opponents. This way we only need to evaluate
  the hand's value once and can reuse the resulting `HandValue` for multiple comparisons.
  '''
  cards = hole_cards + board
  checks_skipped = []
  # It's better to start checking the weaker ranks first since lower hand ranks are more
  # frequent thus it's more probable that we will find a better hand sooner this way.
  for rank in sort_hand_ranks_in_incr_order():
    if rank < compare_to.rank or rank in checks_skipped:
      continue
    check_for_rank = getattr(HandValueWhenRankIsFixedAs, rank.name)
    hand_value = check_for_rank(cards)
    if hand_value is None:
      skip = _STRICTER_VERSIONS_OF_HAND_RANKS.get(rank, [])
      checks_skipped.extend(skip)
      continue
    if compare_to < hand_value:
      return True
  return False
