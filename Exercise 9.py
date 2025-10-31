# My code
# import random

# a = random.randint(1, 9)
# b = int()
# counter = 0
# game = ""

# while game != "exit":
#     b = int(input("Input a random number: "))
#     if b == a:
#         print("You are correct")
#         a = random.randint(1, 9)
#         game = input("type exit to stop")
#     elif b > a:
#         print("Too high")
#         counter += 1
#         game = input("type exit to stop")
#     elif b < a:
#         print("Too low")
#         counter += 1
#         game = input("type exit to stop")

# print("It took you ", counter, "tries")
# counter = 0

import random

rd = random.randint(1,9)
guess = 0
c = 0
while guess != rd and guess != "exit":
    guess = input("Enter a guess between 1 to 9")

    if guess == "exit":
        break

    guess = int(guess)
    c += 1

    if guess < rd:
        print("Too low")
    elif guess > rd:
        print("Too high")
    else:
        print("Right!")
        print("You took only", c, "tries!")
input()