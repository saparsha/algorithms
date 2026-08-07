"""Word Ladder

Shortest chain of single-letter mutations between two words.
"""

from collections import deque
from string import ascii_lowercase


def word_ladder(start, end, words):
    vocab = set(words)
    if end not in vocab:
        return 0
    queue = deque([(start, 1)])
    seen = {start}
    while queue:
        word, depth = queue.popleft()
        if word == end:
            return depth
        for i in range(len(word)):
            for ch in ascii_lowercase:
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in vocab and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, depth + 1))
    return 0


if __name__ == "__main__":
    assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    print("word-ladder: ok")
