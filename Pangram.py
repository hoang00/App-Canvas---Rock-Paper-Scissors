sentence = "thequickbrownfoxjumpsoverthelazydog"

test = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# print(len(test))
value = 0
for i in sentence:
    if i in test:
        value += 1
        test.remove(i)
        # print(test)
        # print(i)
    else:
        pass
print(value)
if value >= 26:
    print("true")
else:
    print("false")