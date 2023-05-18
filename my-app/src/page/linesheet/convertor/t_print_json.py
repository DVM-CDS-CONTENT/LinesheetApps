
import sys
import pandas as pd

jsonData = sys.argv[1]

df = pd.read_json(jsonData)

print(df)