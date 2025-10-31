# Ask the user for a string and print out whether this string is a palindrome or not. (A palindrome is a string that reads the same forwards and backwards.)

# user gives us the input
x = input("Give me a string ")

# we assess the length of the string to know how far to index it. Or we can just do x[:]
y = len(x) - 1

# define the function

if x == x[::-1]:
    print("This is a Palindrome")
else:
    print("This is NOT a Palindrome")
