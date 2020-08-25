from typing import NamedTuple
from enum import Enum, IntEnum

from texas_holdem.utils import NamedTupleWithDocString


class Suit(Enum):
  CLUBS = 'Clubs'
  HEARTS = 'Hearts'
  DIAMONDS = 'Diamonds'
  SPADES = 'Spades'


class Rank(IntEnum):
  ACE_LOW = 1  # Ace that is counted as 1 for the purpose of creating 5 cards of sequential rank
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6
  SEVEN = 7
  EIGHT = 8
  NINE = 9
  TEN = 10
  JACK = 11
  QUEEN = 12
  KING = 13
  ACE = 14


Card = NamedTuple('Card', [('suit', Suit), ('rank', Rank)])


def card_value(card: Card) -> int:
  "Assigns a value to each card based on their rank."
  return card.rank.value


HoleCards = NamedTupleWithDocString(
    'The 2 private cards the player is has.',
    'HoleCards', [('c1', Card), ('c2', Card)]
)


Board = NamedTupleWithDocString(
    'The 5 shared cards (community cards) that every player can use to create their hand.',
    'Board',
    [('c1', Card), ('c2', Card), ('c3', Card), ('c4', Card), ('c5', Card)]
)
