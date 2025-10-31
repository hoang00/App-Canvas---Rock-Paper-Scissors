import pandas as pd
a = [1, 7, 2]
mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}
myvar = pd.Series(a, index = ["x", "y", "z"])

print(myvar)