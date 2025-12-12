# Problem 1: Count Unique Elements in a List
def count_unique(nums):
    # Edge case: empty list
    if not nums:
        return 0
    
    # Use set to remove duplicates
    return len(set(nums))


# Example usage:
example = [1, 2, 2, 3, 4, 4]
print(count_unique(example))  # Output: 4


'''--------------'''



'''# Take user input as a comma-separated list
user_input = input("Enter integers separated by commas: ")

# Edge case: empty input
if not user_input.strip():
    print("0")
else:
    # Convert input string → list of integers
    nums = [int(x) for x in user_input.split(",")]

    # Count unique elements using a set
    unique_count = len(set(nums))

    print("Number of unique elements:", unique_count)'''

