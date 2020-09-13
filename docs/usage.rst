=====
Usage
=====

To use Texas Holdem from command line::

    texas_holdem --hc <your hole cards> --cc <community cards>

Cards are denoted as a combination of a letter representing the suit (S[paded], D[iamonds], C[lubs],
H[earts]) and either a number from 2 to 10 or a letter representing a figure (J[ack], Q[ueen],
K[ing], A[ce]), So 10 of spades is denoted as S10, king of diamonds as DK etc.


To use Texas Holdem in a project::

  # Populates the global namespace with aliases for cards, e.g. SK for king of spades.
  from texas_holdem.shorthand_notations import *
  from texas_holdem import compute_my_chances

  compute_my_chances(hole_cards=[S2, DA], community_cards=[H2, D3, S5, C9])
  # 0.548594642072903
