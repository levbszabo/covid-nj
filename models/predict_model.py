import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
pd.options.display.float_format = '{:.2f}'.format
model_weights = pd.read_excel("models/model_weights.xlsx")
parameters = ["county","days","N","initial","min_c","r0","mean_duration","mean_latency"]
exposed_proj = []
infected_proj = []
county,days,N,initial,min_c,r0,mean_duration,mean_latency = model_weights.loc[0]
def SEIR(t,y):
    S = y[0]
    E = y[1]
    I = y[1]
    R = y[2] 
    d_S = -S/N * (I*r0/mean_duration)   
    d_E =  (S/N * (I*r0/mean_duration)) - (E/mean_latency)
    d_I = E/mean_latency - I/mean_duration
    d_R = I/mean_duration
    return([d_S,d_E,d_I,d_R])
for i in range(len(model_weights)):
    county,days,N,initial,min_c,r0,mean_duration,mean_latency = model_weights.loc[i]
    sol = solve_ivp(SEIR,[0,days+5],[N,min_c*initial,initial,0],t_eval=np.arange(0,days+5))
    exposed_proj.append(np.array(sol.y[1]))
    infected_proj.append(np.array(sol.y[2]))
exposed_df = pd.DataFrame(exposed_proj)
infected_df = pd.DataFrame(infected_proj)
exposed_df.to_csv("data/processed/exposed_output.csv")
infected_df.to_csv("data/processed/infected_output.csv")
