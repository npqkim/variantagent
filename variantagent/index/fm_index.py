def build_occ(bwt, alphabet):
    """
    Build the Occ (occurrence) table for every symbol in alphabet.

    Args:
        bwt (str): The BWT string (already includes the sentinel).
        alphabet (Iterable[str]): Symbols to build rows for, e.g.
            ALPHABET | {SENTINEL}.

    Returns:
        dict[str, list[int]]: occ[c][i] == count of c in bwt[0:i], for
        i in [0, len(bwt)]. occ[c][0] is always 0; occ[c][len(bwt)] is the
        total count of c in the whole bwt.

    Trades O(|alphabet| * n) space (and build time) for O(1) rank lookups,
    replacing the O(n) per-call scan in bwt.rank.
    """
    n = len(bwt)
    occ = {c: [0] * (n + 1) for c in alphabet}
    for i, ch in enumerate(bwt):
        for c in alphabet:
            occ[c][i + 1] = occ[c][i]
        occ[ch][i + 1] += 1
    return occ


def backward_search(pattern, c, occ, sa_len):
    """
    Backward search for pattern using the C array and Occ table.

    Args:
        pattern (str): Query pattern, without the sentinel.
        c (dict[str, int]): C array (build_c), built on the same text as occ.
        occ (dict[str, list[int]]): Occ table (build_occ), built on the same
            bwt as c.
        sa_len (int): Length of the suffix array, i.e. len(text) + 1.

    Returns:
        tuple[int, int]: Half-open range (lo, hi) into the suffix array such
        that sa[lo:hi] are exactly the starting positions of suffixes prefixed
        by pattern, in SA order. If pattern does not occur, lo == hi.

    Invariant: after consuming suffix pattern[i:], (lo, hi) bounds exactly the
    SA range of suffixes prefixed by pattern[i:]. Prepending the next
    character to the left, ch = pattern[i-1], narrows the range via:
        lo = C[ch] + Occ[ch][lo]
        hi = C[ch] + Occ[ch][hi]
    Processing continues right-to-left until the whole pattern is consumed.

    Worked example: pattern="AC" against text="GATTACA".
        sa  = [7, 6, 4, 1, 5, 0, 3, 2]
        bwt = "ACTGA$TA"
        c   = {"$": 0, "A": 1, "C": 4, "G": 5, "T": 6}
        start: lo=0, hi=8 (sa_len)  -- every suffix
        consume 'C' (pattern[1]):
            lo = C['C'] + Occ['C'][0] = 4 + 0 = 4
            hi = C['C'] + Occ['C'][8] = 4 + 1 = 5
            -> (4, 5): sa[4:5] = [5], suffix "CA$"
        consume 'A' (pattern[0]):
            lo = C['A'] + Occ['A'][4] = 1 + 1 = 2
            hi = C['A'] + Occ['A'][5] = 1 + 2 = 3
            -> (2, 3): sa[2:3] = [4], suffix "ACA$"
        Final range (2, 3) is width 1: "AC" occurs once, at text position 4.
    """
    lo, hi = 0, sa_len
    for ch in reversed(pattern):
        if ch not in c:
            return 0, 0
        lo = c[ch] + occ[ch][lo]
        hi = c[ch] + occ[ch][hi]
        if lo >= hi:
            return 0, 0
    return lo, hi
