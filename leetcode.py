from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    for i in range(len(nums)):
        for j in range(i+1, len(nums), 1):
            sum = nums[i] + nums[j]
            print("index {},{} sum is {}".format(i,j,sum))
            if sum == target:
                return [i, j]


twoSum([2, 3, 7, 11], 9)
