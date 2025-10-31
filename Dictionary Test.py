usernames = {}
# num = 5
name = "good_user"
for i in range(0,5):
    usernames[name] = usernames.get(name, 0) +1
print(usernames)