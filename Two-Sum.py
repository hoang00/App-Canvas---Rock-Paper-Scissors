
    # def twoSum(self, nums: List[int], target: int) -> List[int]:
# nums = [2,7,11,15]
# target = 9

# index = 0
# pair_index = {}
# define variables to remember which ones work

# seen = {}
# for i in range(len(nums)):
#     diff = target - nums[i]
#     if diff in seen:
#         [seen[diff], i]
#     else:
#         seen[nums[i]] = i
#         print(seen)

def two_sum_bruteforce(nums, target):
    # Get the length of the list
    n = len(nums)
    
    # Iterate over each pair of indices
    for i in range(n):
        for j in range(i + 1, n):
            # Check if the current pair sums up to the target
            print(i, j)
            if nums[i] + nums[j] == target:
                return [i, j]  # Return the indices of the two numbers
    
    # Return an empty list if no pair is found
    return []

# Example usage:
nums = [15, 7, 11, 2]
target = 9
print(two_sum_bruteforce(nums, target))  # Output: [0, 1]