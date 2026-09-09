
ALPHABET = set("ACGTN")
SENTINEL = "$"


def validate(text):
    # raise if $ already respent
    # raise on chars outside the alphabet
    if SENTINEL in text:
        raise ValueError("Text already contains sentinel character")
    if not all(c in ALPHABET for c in text):
        raise ValueError("Text contains characters outside the alphabet")
    return None  # return NONE or raise bad input

def append_sentinel(text):
    # returns text + "$" 
    return text + SENTINEL;

# O((n^2)logn) for substring comparisons
def build_suffix_array(text):
    validate(text)
    text = append_sentinel(text)
    return sorted(range(len(text)), key=lambda i: text[i:])