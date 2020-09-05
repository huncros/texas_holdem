'List the possible hole cards your opponent can hold that would give them a better hand than yours.'
from typing import List
from itertools import combinations

from texas_holdem.card import HoleCards, Board, Card, list_all_cards
from texas_holdem.evaluate_hand import get_hand_value
from texas_holdem.compare_hands import has_better_hand_than_hand_value


def find_better_hole_cards(my_hole_cards: HoleCards, board: Board) -> List[HoleCards]:
  '''Returns the list of the possible hole cards your opponent can hold that would give them a
  better hand than your.
  '''
  my_hand_value = get_hand_value(my_hole_cards, board)
  better_hole_cards = []
  cards_seen = my_hole_cards + board
  remaining_cards = list_remaining_cards(cards_seen)
  for c1, c2 in combinations(remaining_cards, 2):
    opponent_hole_cards = HoleCards(c1, c2)
    if has_better_hand_than_hand_value(opponent_hole_cards, board, my_hand_value):
      better_hole_cards.append(opponent_hole_cards)
  return better_hole_cards


def list_remaining_cards(cards_seen):
  return [card for card in list_all_cards() if card not in cards_seen]
