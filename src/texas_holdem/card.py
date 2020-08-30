from typing import NamedTuple
from enum import Enum, IntEnum


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


class Card(NamedTuple):
  suit: Suit
  rank: Rank


def card_value(card: Card) -> int:
  "Assigns a value to each card based on their rank."
  return card.rank.value


class HoleCards(NamedTuple):
  'The 2 private cards the player has.'
  c1: Card
  c2: Card


class Board(NamedTuple):
  'The 5 shared cards (community cards) that every player can use to create their hand.'
  c1: Card
  c2: Card
  c3: Card
  c4: Card
  c5: Card
