"""Trapping Rain Water

Volume of water trapped between bars, using two pointers.
"""

def trap(heights):
    lo, hi = 0, len(heights) - 1
    left_max = right_max = total = 0
    while lo < hi:
        if heights[lo] < heights[hi]:
            left_max = max(left_max, heights[lo])
            total += left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            total += right_max - heights[hi]
            hi -= 1
    return total


if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([]) == 0
    print("trapping-rain-water: ok")
