from collections import Counter
from .suffix_array import validate, append_sentinel, SENTINEL


def build_bwt(text, sa):
    """
    build bwt from text and suffix array
    Args:
        text (str): The raw input string, WITHOUT the sentinel — build_bwt appends it.
        sa (list[int]): Suffix array of text produced by build_suffix_array(text).
    Returns:
        str: The BWT of the input string.
    """
    validate(text)
    text = append_sentinel(text)
    bwt = []
    for i in sa:
        if i == 0:
            bwt.append(SENTINEL)
        else:
            bwt.append(text[i - 1])
    return ''.join(bwt)

def build_c(text):
    """
    build c from text
    Args:
        text (str): The raw input string, WITHOUT the sentinel — build_c appends it.
    Returns:
        dict: The C array of the input string.
    """

    validate(text)
    text = append_sentinel(text)
    counts = Counter(text)

    # walk symbols in sorted order
    c = {}
    total = 0
    for symbol in sorted(counts.keys()):
        c[symbol] = total
        total += counts[symbol]
    return c

def rank(bwt, char, i):
    """
    count occurrences of char in bwt[0:i]
    Args:
        bwt (str): The BWT of the input string.
        char (str): The character to count.
        i (int): Exclusive upper bound of the range to count within.
    Returns:
        int: Number of occurrences of char in bwt[0:i].
    """
    return bwt[:i].count(char)


def lf(bwt, c, i):
    """
    compute LF mapping
    Args:
        bwt (str): The BWT of the input string.
        c (dict): The C array of the input string.
        i (int): Index in the BWT to map from.
    Returns:
        int: Index in the BWT to map to.
    """
    return c[bwt[i]] + rank(bwt, bwt[i], i)

def inverse_bwt(bwt, c):
    """
    compute inverse BWT
    Args:
        bwt (str): The BWT of the input string.
        c (dict): The C array of the input string.
    Returns:
        str: The original input string, WITHOUT the sentinel.
    """
    n = len(bwt)
    text = []
    i = bwt.index(SENTINEL)
    for _ in range(n - 1):
        i = lf(bwt, c, i)
        text.append(bwt[i])
    return ''.join(reversed(text))
