from abc import ABC, abstractmethod
from functools import reduce
from multiprocessing import Pool
import operator as op
from itertools import combinations
from statistics import mean
from typing import Sequence, Tuple, Dict, Optional

from texas_holdem.card import Card, HoleCards, Board, list_remaining_cards
from texas_holdem.find_better_hole_cards import find_better_hole_cards


class Opponent(ABC):
  '''Represents the assumptions we have about the opponent's hole card.

  E.g. based on their betting pattern or behavior we can assume how likely it is that they
  have a certain hand or better.

  These assumptions can be included in the calculation of your chances against the opponent.
  To do this, subclass this class and overwrite the `hole_card_weight` method to return a
  non-negative weight representing the assumed likeliness of each scenario.
  '''
  @abstractmethod
  def hole_card_weight(self, opponents_hole_cards: HoleCards, board: Board) -> float:
    pass


class OpponentError(Exception):
  def __init__(self, msg):
    base_msg = 'An error occured while trying to use assumptions to compute your chances: '
    if msg is None:
      msg = base_msg
    else:
      msg = base_msg + msg
    super().__init__(msg)


def compute(
    hole_cards: Sequence[Card], community_cards: Sequence[Card],
    against: Optional[Opponent] = None) -> float:
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
  possible_boards = _list_possible_boards(hole_cards_, community_cards_)

  worker_args = ((hole_cards_, board, _compute_weights(hole_cards_, board, against))
      for board in possible_boards)

  with Pool() as p:
    partition_results = p.starmap(worker, worker_args)

  weighted_bad_cases = sum(r['bad'] for r in partition_results)
  weighted_all_cases = sum(r['all'] for r in partition_results)
  if weighted_all_cases == 0:
    raise OpponentError(
        'The `hole_card_weights` method of your `Opponent` instance returns 0 for every possible ' +
        'hole cards the opponent can have. Change the method so at least one possible hole cards ' +
        'receive positive weight.'
    )
  opp_chance_for_better_hole_cards = weighted_bad_cases / weighted_all_cases
  return  1 - opp_chance_for_better_hole_cards


def worker(hole_cards: HoleCards, board: Board, weights: Optional[Dict[HoleCards, int]]):
  better_hole_cards = find_better_hole_cards(hole_cards, board)
  if weights is None:
    weighted_bad_cases = len(better_hole_cards)
    weighted_all_cases = n_choose_m(45, 2)
  else:
    weighted_bad_cases = sum(weights[hc] for hc in better_hole_cards)
    weighted_all_cases = sum(weights.values())
  return {'bad': weighted_bad_cases, 'all': weighted_all_cases}


def _compute_weights(hole_cards: HoleCards, board: Board, opp=None):
  if opp is None:
    return
  weights = {hc: opp.hole_card_weight(hc, board) for hc
      in _list_possible_opp_hole_cards(hole_cards, board)}
  negative_weights = {hc: w for hc, w in weights.items() if w < 0}
  if len(negative_weights) > 0:
    msg = (
        'The `hole_card_weights` method of your `Opponent` instance returns negative weights for ' +
        'the following hole cards:\n')
    for hc, w in negative_weights.items():
      msg += f'  {hc}: {w}\n'
    raise OpponentError(msg)
  return weights


def _list_possible_opp_hole_cards(hole_cards: HoleCards, board: Board):
  cards_seen = hole_cards + board
  remaining_cards = list_remaining_cards(cards_seen)
  return (HoleCards(*c) for c in combinations(remaining_cards, 2))


def _list_possible_boards(hole_cards, community_cards):
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
