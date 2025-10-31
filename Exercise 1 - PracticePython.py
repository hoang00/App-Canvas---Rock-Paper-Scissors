# Input function to determine how many years until I am 100

name = input("Give me your name: ")
age = int(input("Give me your age: "))
# error messaging to prevent others from putting negative age
if age <= 0:
    print("error: Cannot put in a negative number")
if age > 100:
    print("error: Cannot put in a number over 100")
elif age > 0:
    year = 2024 - age + 100 
    print("Hello my name is {} and my age is {}\n. I expect to be 100 in {}".format(name, age, year))