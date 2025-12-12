def is_balanced(s):
    stack = []

    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:        # no matching opening bracket
                return False
            stack.pop()

    # If stack is empty → all opened parentheses were closed
    return len(stack) == 0


# Examples
print(is_balanced("(()())"))  # True
print(is_balanced(""))        # True 
print(is_balanced("(()"))     # False
print(is_balanced("())("))    # False

'''---------------------------'''

'''def is_balanced(s):
    stack = []

    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:        # no matching opening '('
                return False
            stack.pop()

    return len(stack) == 0      # empty stack → balanced


# ------- User Input -------
user_input = input("Enter a string of parentheses: ")

# Edge case: empty string → true
if user_input.strip() == "":
    print("True")
else:
    print("True" if is_balanced(user_input) else "False")'''

