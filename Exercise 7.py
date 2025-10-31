import random

a = random.sample(range(1, 100), 10)

# original list
# a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# overall logic on how it should work
# b= []
# def func():
#     for even in a:
#         # print(even)
#         if even % 2 ==0:
#             b.append(even)
#     return(even)
# func()
# print(b)

# one line solution
print([x for x in a if x % 2 ==0])
