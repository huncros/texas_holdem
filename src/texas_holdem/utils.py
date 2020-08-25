from typing import NamedTuple


def NamedTupleWithDocString(docstring, *ntargs):
  """Creates a NamedTuple instance using the `ntargs` parameters and adds docsting to it.

  In python3.5 the way to create NamedTuples with type hints is

      XXX = NamedTuple('XXX'), [(field1, type1), ..., (fieldN, typeN)])

  This doesn't allow docstrings. This function solves that problem by modifying modifying the
  `__doc__` attribute of the created NamedTuple instance.
  """
  nt = NamedTuple(*ntargs)
  nt.__doc__ = docstring
  return nt
