'''Populates the global namespace with aliases for the cards.

E.g. SK for Card(suit=Suit.SPADES, rank=Rank.KING).

Usage
-----

    >>> from shorthand_notations import *
'''
from texas_holdem.card import Rank, list_all_cards


aliases = []
for card in list_all_cards():
  globals()[str(card)] = card
  aliases.append(str(card))


__all__ = aliases
