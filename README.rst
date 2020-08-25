========
Overview
========

Calculates your chances when playing Texas holdem poker.

More precisely: **calculcate the probability that after all community cards have been dealt you will
have a hand not weaker than the player sitting across you.**

Of course the "player sitting across you" can be replaced with any of the opponents.

The advantages of using this metric to determine your chances:

  - It captures the most important information of whether you are the favorite to win.
    This is because with N players, you have at least 1/N probability to win if and only if your
    chance of beating the player sitting across you is at least 0.5.
  - Thus it's easy to understand. If you have 0.6 chance to beat the player sitting across you
    then you are the favorite of this round of the game regardless of how many other players are
    there.
  - The computation does not depend on the number of players thus its complexity and runtime
    speed is the same regardless if there is one opponent or ten.
  - We compute the chance of beating the player sitting across you by computing their possible
    hole card combinations with which they would have a stronger hand and then dividing number of
    such hole card combinations with the number of all possible hole card combinations they can
    have.
    This approach makes it easy to create higher-level strategies that include additional
    information or assumptions in our computation.
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
