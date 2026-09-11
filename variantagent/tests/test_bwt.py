import random

from index.bwt import build_bwt, build_c, inverse_bwt, lf, rank
from index.suffix_array import build_suffix_array


def test_build_bwt_banana():
    text = "ACGT"
    sa = build_suffix_array(text)
    assert build_bwt(text, sa) == "T$ACG"


def test_build_bwt_all_same_character():
    text = "AAAA"
    sa = build_suffix_array(text)
    assert build_bwt(text, sa) == "AAAA$"


def test_build_c_counts_and_ordering():
    # "$" < "A" < "C" < "G" < "T" in the C array's sort order
    c = build_c("ACGT")
    assert c == {"$": 0, "A": 1, "C": 2, "G": 3, "T": 4}


def test_rank_counts_occurrences_before_index():
    bwt = "TGCA$"
    assert rank(bwt, "T", 0) == 0
    assert rank(bwt, "T", 1) == 1
    assert rank(bwt, "T", len(bwt)) == 1
    assert rank(bwt, "A", len(bwt)) == 1
    assert rank(bwt, "N", len(bwt)) == 0


def test_rank_is_exclusive_of_i():
    bwt = "AAAA"
    assert rank(bwt, "A", 2) == 2
    assert rank(bwt, "A", 0) == 0


def test_lf_matches_hand_computed_example():
    # text="ACGT", full="ACGT$", sa=[4, 0, 1, 2, 3], bwt="T$ACG"
    bwt = "T$ACG"
    c = build_c("ACGT")
    assert lf(bwt, c, 1) == 0  # bwt[1] == "$"
    assert lf(bwt, c, 0) == 4  # bwt[0] == "T"
    assert lf(bwt, c, 4) == 3  # bwt[4] == "G"
    assert lf(bwt, c, 3) == 2  # bwt[3] == "C"
    assert lf(bwt, c, 2) == 1  # bwt[2] == "A"


def test_inverse_bwt_recovers_original_text():
    text = "ACGT"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    assert inverse_bwt(bwt, c) == text


def test_inverse_bwt_empty_string():
    assert inverse_bwt("$", build_c("")) == ""


def test_inverse_bwt_all_same_character():
    text = "AAAA"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    assert inverse_bwt(bwt, c) == text


def test_inverse_bwt_round_trip_random():
    rng = random.Random(42)
    for _ in range(50):
        length = rng.randint(1, 30)
        text = "".join(rng.choice("ACGT") for _ in range(length))
        sa = build_suffix_array(text)
        bwt = build_bwt(text, sa)
        c = build_c(text)
        assert inverse_bwt(bwt, c) == text
