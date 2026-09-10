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

from collections import Counter
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
    
