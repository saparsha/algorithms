"""Factorial

Iterative factorial with input validation.
"""

def factorial(n):
    if n < 0:
        raise ValueError("negative input")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    assert factorial(0) == 1
    assert factorial(5) == 120
    print("factorial: ok")
