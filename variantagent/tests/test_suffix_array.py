import random

import pytest

from index import suffix_array
from index.suffix_array import build_suffix_array, validate


def test_banana_classic_example(monkeypatch):
    # Classic Manber-Myers example. ALPHABET is ACGTN-only in prod, so widen
    # it just for this test; monkeypatch reverts it automatically afterward.
    monkeypatch.setattr(suffix_array, "ALPHABET", set("banana$"))
    assert build_suffix_array("banana") == [6, 5, 3, 1, 0, 4, 2]


def test_empty_string():
    assert build_suffix_array("") == [0]


def test_single_character():
    assert build_suffix_array("A") == [1, 0]


def test_random_acgt_strings_against_oracle():
    def oracle(text_with_sentinel):
        n = len(text_with_sentinel)
        return sorted(range(n), key=lambda i: text_with_sentinel[i:])

    rng = random.Random(42)
    for _ in range(50):
        length = rng.randint(1, 30)
        text = "".join(rng.choice("ACGT") for _ in range(length))
        assert build_suffix_array(text) == oracle(text + "$")


def test_all_same_character():
    assert build_suffix_array("AAAAAA") == [6, 5, 4, 3, 2, 1, 0]


def test_validate_raises_on_sentinel_in_input():
    with pytest.raises(ValueError):
        validate("AC$GT")
