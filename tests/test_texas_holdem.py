#!/usr/bin/env python

"""Tests for `texas_holdem` package."""


import unittest

from texas_holdem import texas_holdem


class TestTexas_holdem(unittest.TestCase):
    """Tests for `texas_holdem` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_add(self):
      s = texas_holdem.add(1,2)
      self.assertEqual(s,3)
