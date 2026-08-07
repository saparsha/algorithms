"""Word Frequency

Count word occurrences, case-insensitively, ignoring punctuation.
"""

import re
from collections import Counter


def word_frequency(text):
    return Counter(re.findall(r"[a-z0-9']+", text.lower()))


if __name__ == "__main__":
    f = word_frequency("The cat. The CAT!")
    assert f["the"] == 2 and f["cat"] == 2
    print("word-frequency: ok")
