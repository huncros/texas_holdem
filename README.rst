========
Overview
========

Calculate your chances when playing Texas holdem poker.

More precisely: **calculcate the probability that after all community cards have been dealt you will
have a hand not weaker than the guy sitting across you.**

TODO: explain why use this metric and its advantages.


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
