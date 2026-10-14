## Problem 2: Remove Duplicates
# Write a function that removes duplicate elements from a list while preserving their original order.

def remove_duplicates(lst):

    # Creating an eempty list for unique elements.
    unique_list = []

    # Loop through every item in lst.
    for item in lst:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list

# Test for output
lst = [4, 2, 4, 1, 2, 5]
print(remove_duplicates(lst))