# Compare two versions and return the comparison result.
# if v1 is newer than v2, return -1
# if v1 is older than v2, return 1
# if v1 is the same with v2, return 0

# You can assume:
# 1. all digits in the versions are greater or equal to 0
# 2. the inputs will be valid strings

def compareVersion(v1, v2):
    # cur_v1 = ""
    # cur_v2 = ""
# status is the value we want to return
    status = "0"
# quick check to see if it equivalent and we can end early
    if v1 == v2:
        return status
# compare the two items
    else:
    # split into list
        v1 = v1.split(".")
        v2 = v2.split(".")
    # compare lengths
        diff = len(v1) - len(v2)
    # if lengths are different, add zeroes to the list such that length is equal
        if diff > 0:
            for i in range(abs(diff)):
                v2.append("0")
        elif diff < 0:
            for i in range(abs(diff)):
                v1.append("0")

    # once lengths are equal, we can use the zip function to iterate and compare between the two lists
        for x, y in zip(v1, v2):
    # continue iterating IF the status value is still 0; break out if there is a difference
            if x == y:
                status = 0
            if x > y:
                status = "-1"
                return status
            elif x < y:
                status = "1"
                return status
        pass
    
print(compareVersion("1.0.0", "1.0.1"))       # 1
print(compareVersion("1", "1.0.0"))           # 0
print(compareVersion("2.0.1", "2.0.10"))      # 1
print(compareVersion("1.0.0", "2.0.0.13"))    # 1
print(compareVersion("18.0", "0.0.0.4"))      # -1
print(compareVersion("1.0.1.23", "1.0.11.1")) # 1
print(compareVersion("1.0.1.23", "1.0"))      # -1
print(compareVersion("1.0.0", "1.0"))         # 0
print(compareVersion("1.0.0.0", "1.0"))       # 0
print(compareVersion("1.0.0.2", "1.0"))       # -1
print(compareVersion("1.10.0.2", "1.2.0"))    # -1