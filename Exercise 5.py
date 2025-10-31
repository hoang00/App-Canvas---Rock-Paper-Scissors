import random

a = random.sample(range(1, 100), 10)
b = random.sample(range(1, 100), 15)

c = []

def func(x, y):
    for item in a:
        if item in b:
            c.append(item)
        else:
            pass
    print(c)


func(a, b)