# Return the first non-repeating character in a string.
def first_non_repeating_char(s):
    freq = {}

    # Count frequency
    for char in s:
        freq[char] = freq.get(char, 0) + 1

    # Find first non-repeating
    for char in s:
        if freq[char] == 1:
            return char

    return None


# ---- Fixed Input Example ----
s = "aabbccddee"
result = first_non_repeating_char(s)
print("Input:", s)
print("First non-repeating character:",result)

'''-----------------------------'''

#user input
'''def first_non_repeating_char(s):
    freq = {}

    # Count frequency of each character
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    # Find the first non-repeating character
    for ch in s:
        if freq[ch] == 1:
            return ch

    return None  # if none exist


# --- User Input ---
s = input("Enter a string: ")

result = first_non_repeating_char(s)
print("Output:", result)'''




