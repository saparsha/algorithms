"""Z-Function

For each position, the length of the longest prefix match starting there.
"""

def z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    if n:
        z[0] = n
    return z


if __name__ == "__main__":
    assert z_function("aaaaa") == [5, 4, 3, 2, 1]
    assert z_function("") == []
    print("z-function: ok")
