# This function asks a user for a number - depending on whether the number is even or odd, print out an appropriate number

def myfunction(number):
    # If a number is dividable by 2, there will be no remainder
    if number % 2 == 0:
        print("this is an even number")
    if number % 2 != 0:
        print("this is an odd number")
myfunction(4)