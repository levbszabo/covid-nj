import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.2f}'.format
corona_NJ = pd.read_excel("data/raw/nj_raw.xlsx")
corona_NJ = corona_NJ.transpose()
dataset = corona_NJ.values[1:-1,:]
#def ff(num):
#   return np.format_float_positional(np.round(num,4), trim='-')
data = []
for ar in dataset:
    data.append(ar[0:-5])
df = pd.DataFrame(data)
df.to_excel("data/processed/nj_clean.xlsx")