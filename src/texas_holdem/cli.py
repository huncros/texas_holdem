"""Console script for texas_holdem."""
import argparse
import sys

from texas_holdem.card import parse
from texas_holdem.my_chances import compute


def main():
    """Console script for texas_holdem."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--hole_cards',
      '--hc',
      nargs=2,
      required=True,
      type=parse)
    parser.add_argument(
      '--community_cards',
      '--cc',
      nargs='*',
      type=parse)

    args = parser.parse_args()

    my_chances = compute(args.hole_cards, args.community_cards)
    print(my_chances)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
