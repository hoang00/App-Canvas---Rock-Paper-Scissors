# iterate through the lists (maybe see which one is longer?)
# whichover one is longer will be used for the 
# add each position with each other
# incorporate overflow from one position to the next

# l1 = [9,9,9,9,9,9,9]
# l2 = [9,9,9,9]

l1 = []
l2 = []
diff = len(l1) - len(l2)
sum = []
counter = 0
value = 0
remainder = 0

# test = 12
# print(test //10**0 % 10)

# if l1 is longer than l2; iterate over l2
if diff > 0:
    for i in enumerate(l2):
# add numbers + remainder(if exists)
        value = i[1] + l1[counter] + remainder
# if value is greater than 10, we must store a remainder
        if value >= 10:
# store remainder to move onto next iteration
            remainder = value //10**1 % 10
# append value to current position
            sum.append((value //10**0 % 10))
# if value is less than 10, we just store value in the position
        elif value < 10:
            sum.append(value)
            remainder = 0
        counter += 1
# iterate through the rest of the values contained in the longer list...
    for f in enumerate(l1[len(l2)::]):
        value = remainder + f[1]
        if value >= 10:
# store remainder to move onto next iteration
            remainder = value //10**1 % 10
# append value to current position
            sum.append((value //10**0 % 10))
# if value is less than 10, we just store value in the position
        elif value < 10:
            sum.append(value)
            remainder = 0
    if remainder != 0:
        sum.append(remainder)
        print(sum)


if diff < 0:
    for i in enumerate(l1):
# add numbers + remainder(if exists)
        value = i[1] + l2[counter] + remainder
# if value is greater than 10, we must store a remainder
        if value >= 10:
# store remainder to move onto next iteration
            remainder = value //10**1 % 10
# append value to current position
            sum.append((value //10**0 % 10))
# if value is less than 10, we just store value in the position
        elif value < 10:
            sum.append(value)
            remainder = 0
        counter += 1
# iterate through the rest of the values contained in the longer list...
    for f in enumerate(l2[len(l1)::]):
        value = remainder + f[1]
        if value >= 10:
# store remainder to move onto next iteration
            remainder = value //10**1 % 10
# append value to current position
            sum.append((value //10**0 % 10))
# if value is less than 10, we just store value in the position
        elif value < 10:
            sum.append(value)
            remainder = 0
    if remainder != 0:
        sum.append(remainder)
        print(sum)