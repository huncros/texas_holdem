from functools import reduce
from multiprocessing import Pool
import operator as op
from itertools import combinations
from statistics import mean
from typing import Sequence, Tuple

from texas_holdem.card import Card, HoleCards, Board, list_remaining_cards
from texas_holdem.find_better_hole_cards import find_better_hole_cards


def compute(hole_cards: Sequence[Card], community_cards: Sequence[Card]):
  '''Computes the probabilty that when all 5 community cards are dealt you will have a hand not
  weaker than the player sitting across you.

  The "player sitting across you" can be replaced with any of your opponents.

  Knowing your chances against any of your opponets is intuitively also a good heuristic to gauge
  your chances in case of multiple opponents while being much easier to compute compared to the
  probability that none of your opponents having a better hand than you.
  '''
  assert len(hole_cards) == 2, f'Needs exactly 2 hole cards. Got: {len(hole_cards)}.'
  assert len(community_cards) in (0, 3, 4, 5), (
      f'There can be either 0, 3, 4 or 5 community cards revealed. Got: {len(community_cards)}.')
  hole_cards_ = HoleCards(*hole_cards)
  community_cards_ = tuple(community_cards)
  possible_boards = list_possible_boards(hole_cards_, community_cards_)
  possible_cards_seen = ((hole_cards_, board) for board in possible_boards)

  with Pool() as p:
    avg_better_hole_cards = mean(p.map(worker, possible_cards_seen))

  num_possible_hole_cards = n_choose_m(45, 2)
  return  1 - (avg_better_hole_cards / num_possible_hole_cards)


def worker(cards_seen):
  hole_cards, board = cards_seen
  return len(find_better_hole_cards(hole_cards, board))


def list_possible_boards(hole_cards, community_cards):
  cards_seen = hole_cards + community_cards
  remaining_cards = list_remaining_cards(cards_seen)
  num_missing_cards = 5 - len(community_cards)
  return (Board(*(community_cards + cards))
      for cards in combinations(remaining_cards, num_missing_cards))


def n_choose_m(n: int, m: int):
  m = min(m, n - m)
  numer = reduce(op.mul, range(n, n - m, -1))
  denom = reduce(op.mul, range(1, m + 1))
  return numer // denom
