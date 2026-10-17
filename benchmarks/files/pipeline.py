from typing import List


def double_it(x: int) -> int:
    return x * 2


def add_ten(x: int) -> int:
    return x + 10


def process(x: int) -> int:
    return add_ten(double_it(x))


def process_all(nums: List[int]) -> List[int]:
    return [process(n) for n in nums]
