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

::

    pip install git+git://github.com/huncros/texas-holdem.git#egg=texas-holdem


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
