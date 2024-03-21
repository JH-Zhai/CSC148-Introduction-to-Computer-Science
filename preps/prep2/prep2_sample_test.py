"""Prep 2 Synthesize Sample Tests

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains sample tests for Prep 2.
Add your own tests to practice writing tests and to be confident your code is
correct.

WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
We will test your code on a much more thorough set of tests!

For more information on hypothesis (one of the testing libraries we're using),
please see
<https://www.teach.cs.toronto.edu/~csc148h/fall/notes/testing/hypothesis.html>
"""
from hypothesis import given
from hypothesis.strategies import integers
from prep2 import Spinner


# This is a hypothesis test; it generates a random integer to use as input,
# so that we don't need to hard-code a specific number of slots in the test.
@given(slots=integers(min_value=1))
def test_new_spinner_position(slots: int) -> None:
    """Test that the position of a new spinner is always 0."""
    spinner = Spinner(slots)
    assert spinner.position == 0


def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0


def test_zeroforce() -> None:
    # Test if the givien force to spin arrow is zero
    spinner = Spinner(8)
    spinner.spin(0)
    assert spinner.position == 0


def test_ifHaevyForce() -> None:
    # Test if the given force to spin the arrow is super big
    spinner = Spinner(10)
    spinner.spin(1001)
    assert spinner.position == 1


if __name__ == '__main__':
    import pytest

    pytest.main(['prep2_sample_test.py'])
