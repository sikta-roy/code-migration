import math

def square(x: int) -> int:
    return x * x

def sum_squares(nums):
    total = 0
    for n in nums:
        total += square(n)
    return total

def mean_square(nums):
    if not nums:
        return 0.0
    return sum_squares(nums) / len(nums)
