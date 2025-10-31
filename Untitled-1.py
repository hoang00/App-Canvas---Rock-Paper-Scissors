s = "abcdeabc"

# l1 = []
# counter = 0
# highscore = 0
# # loop through the string
# for i in st:
#     if i not in l1:
#         l1.append(i)
#         counter += 1
#         if counter > highscore:
#             highscore = counter
#     elif i in l1:
#         l1.clear()
#         if counter > highscore:
#             highscore = counter
#             counter = 1
#         else:
#             counter = 1
#     print("Counter", counter)
#     print(highscore)
# print(highscore)

seen = {}
l = 0
output = 0
for r in range(len(s)):
    if s[r] not in seen:
        output = max(output,r-l+1)
    else:
        if seen[s[r]] < l:
            output = max(output,r-l+1)
        else:
            l = seen[s[r]] + 1
    seen[s[r]] = r
    print(seen)
    print(seen[s])
