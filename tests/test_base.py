"""Test base.py module."""

from pyschemes import Scheme


def test_scheme():
    Scheme(int).validate(10)
