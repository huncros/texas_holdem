========
Overview
========

Calculates your chances when playing Texas holdem poker.

More precisely: **calculcate the probability that after all community cards have been dealt you will
have a hand not weaker than the player sitting across you.**

Of course the "player sitting across you" can be replaced with any of the opponents.

The motivation behind choosing this metric to determine your chances:

  - When trying to calculate the probability that none of your opponents has a better hand, the
    even space can become very big very quickly - e.g. even when all 5 community cards have already
    been revealed and there are only 3 opponents, the number of possible deals are
    (45 choose 2) * (43 choose 2) * (41 choose 2), which is over 700M cases.
  - On the other hand, by only checking our chances against one opponent, the event space is
    sufficiently restricted - regardless if we have one opponents or ten.
  - Knowing your chances against any of your opponents is intuitively a good heuristic to
    gauge your chances in case of multiple opponents.
  - By having a sufficiently small event space, we can check all cases instead of needing to use
    some kind of sampling method.
    This also makes it easy to extend our approach to create higher-level strategies that include
    additional information or assumptions in our computation.
    E.g. based on the bets the player did we can make assumptions about his hand and
    assume that they can only some of the hole cards and not all of them.


Installation
============

To install Texas holdem, run this command in your terminal::

    pip install git+https://github.com/huncros/texas_holdem.git#egg=texas_holdem


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


Development
===========

To set up the development environment run::

    make dev-env

This will set up the pre-commit hook, create a python virtual env that is used to run the tools
that are used for development / testing.

To run all the tests run::

    make test

To check the test coverage run::

    make coverage

To build documentation run::

    make docs


Code style
----------

The project follows pep8 with the exception of having 2 space indentations and max line length
being 100.
The code style is enforced by the pre-commit hook that runs autopep8 on the staged python files.


Terminology
-----------

The terminology in the code tries to follow the Texas Holdem terminology. If you are not familiar
with some of the terms used, please consult the glossary.
