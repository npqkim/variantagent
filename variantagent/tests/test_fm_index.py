from index.bwt import build_bwt, build_c
from index.fm_index import backward_search, build_occ
from index.suffix_array import ALPHABET, SENTINEL, build_suffix_array


def test_build_occ_prefix_counts():
    bwt = "T$ACG"
    occ = build_occ(bwt, ALPHABET | {SENTINEL})
    assert occ["T"] == [0, 1, 1, 1, 1, 1]
    assert occ["$"] == [0, 0, 1, 1, 1, 1]
    assert occ["A"] == [0, 0, 0, 1, 1, 1]
    assert occ["C"] == [0, 0, 0, 0, 1, 1]
    assert occ["G"] == [0, 0, 0, 0, 0, 1]


def test_build_occ_zero_at_start():
    bwt = "ACTGA$TA"
    occ = build_occ(bwt, ALPHABET | {SENTINEL})
    for c in occ:
        assert occ[c][0] == 0
        assert occ[c][len(bwt)] == bwt.count(c)


def test_backward_search_gattaca_single_match():
    text = "GATTACA"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    occ = build_occ(bwt, ALPHABET | {SENTINEL})

    lo, hi = backward_search("AC", c, occ, len(bwt))
    assert (lo, hi) == (2, 3)
    assert [sa[i] for i in range(lo, hi)] == [4]


def test_backward_search_multiple_matches():
    text = "GATTACA"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    occ = build_occ(bwt, ALPHABET | {SENTINEL})

    lo, hi = backward_search("A", c, occ, len(bwt))
    assert sorted(sa[i] for i in range(lo, hi)) == [1, 4, 6]


def test_backward_search_no_match():
    text = "GATTACA"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    occ = build_occ(bwt, ALPHABET | {SENTINEL})

    assert backward_search("CG", c, occ, len(bwt)) == (0, 0)


def test_backward_search_empty_pattern_matches_everything():
    text = "GATTACA"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c = build_c(text)
    occ = build_occ(bwt, ALPHABET | {SENTINEL})

    assert backward_search("", c, occ, len(bwt)) == (0, len(bwt))
