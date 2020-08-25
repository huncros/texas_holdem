'''Populates the global namespace with aliases for the cards.

E.g. SK for Card(suit=Suit.SPADES, rank=Rank.KING).

Usage
-----

    >>> from shorthand_notations import *
'''
from texas_holdem.card import Card, Rank, Suit


for suit in Suit:
  for rank in Rank:
    if rank == Rank.ACE_LOW:
      # ACE and ACE_LOW are the same card with the difference being whether we consider ACE
      # as the rank following KING or preceding TWO.
      continue
    rank_alias = str(rank.value) if rank <= Rank.TEN else rank.name[0]
    alias = suit.name[0] + rank_alias
    globals()[alias] = Card(rank=rank, suit=suit)
