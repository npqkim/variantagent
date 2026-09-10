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
