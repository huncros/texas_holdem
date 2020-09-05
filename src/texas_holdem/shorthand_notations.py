'''Populates the global namespace with aliases for the cards.

E.g. SK for Card(suit=Suit.SPADES, rank=Rank.KING).

Usage
-----

    >>> from shorthand_notations import *
'''
from texas_holdem.card import Rank, list_all_cards


aliases = []
for card in list_all_cards():
  rank_alias = str(card.rank.value) if card.rank <= Rank.TEN else card.rank.name[0]
  alias = card.suit.name[0] + rank_alias
  globals()[alias] = card
  aliases.append(alias)


__all__ = aliases
