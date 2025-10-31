# x = 121
# # x = -121

# forward = str(x)
# reverse = ""
# for i in range(len(forward)-1, -1, -1):
#     reverse += forward[i]
# print(reverse)
# if forward == str(reverse):
#     print("true")
# else:
#     print("false")

l1 = [1,2,3]
l2 = [1,2,3]
l3 = [1]
l3[0] = (l1[1] + l2[1])
print(l3)