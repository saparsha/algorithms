"""Smart Title Case

Capitalise words except common short joining words, always keeping the first.
"""

MINOR = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to"}


def title_case(s):
    words = s.lower().split()
    return " ".join(
        w.capitalize() if i == 0 or w not in MINOR else w for i, w in enumerate(words)
    )


if __name__ == "__main__":
    assert title_case("the lord of the rings") == "The Lord of the Rings"
    assert title_case("hello brave world") == "Hello Brave World"
    print("title-case: ok")
