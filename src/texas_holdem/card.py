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
  def __str__(self):
    rank_alias = str(self.rank.value) if self.rank <= Rank.TEN else self.rank.name[0]
    return self.suit.name[0] + rank_alias


def parse(card_alias: str) -> Card:
  '''Takes a shorthand notation of a card (e.g. S10 or DA for 10 of spades or ace of diamonds) and
  returns a correspoding Card instance.
  '''
  suit_alias = card_alias[0]
  suit = next(s for s in Suit if s.value.startswith(suit_alias))
  rank_alias = card_alias[1:]
  try:
    rank_value = int(rank_alias)
  except:
    rank_value = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank_alias]
  rank = next(r for r in Rank if r.value == rank_value)
  return Card(suit=suit, rank=rank)


def card_value(card: Card) -> int:
  "Assigns a value to each card based on their rank."
  return card.rank.value


def list_all_cards():
  'A generator listing all the cards in the deck.'
  for suit in Suit:
    for rank in Rank:
      if rank == Rank.ACE_LOW:
        # ACE and ACE_LOW are the same card with the difference being whether we consider ACE
        # as the rank following KING or preceding TWO.
        continue
      yield Card(suit=suit, rank=rank)


def list_remaining_cards(cards_seen):
  return [card for card in list_all_cards() if card not in cards_seen]


class HoleCards(NamedTuple):
  'The 2 private cards the player has.'
  c1: Card
  c2: Card

  def __eq__(self, other):
    return set(self) == set(other)

  def __str__(self):
    c1, c2 = sorted([str(self.c1), str(self.c2)])
    return f'HoleCards({c1},{c2})'

  def __hash__(self):
    return hash(str(self))


class Board(NamedTuple):
  'The 5 shared cards (community cards) that every player can use to create their hand.'
  c1: Card
  c2: Card
  c3: Card
  c4: Card
  c5: Card
