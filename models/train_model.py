import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
pd.options.display.float_format = '{:.2f}'.format
dataset = pd.read_excel("data/processed/nj_clean.xlsx")
parameters = ["county","days","N","initial","min_c","r0","mean_duration","mean_latency"]
model_df = pd.DataFrame(columns = parameters)
for i in range(16):
    county = dataset.loc[i].values[0]
    time_series = dataset.loc[i].values[1:]
    time_series = time_series[time_series>1]
    max_pop = time_series[-1]
    if max_pop > 50:   
        N = 10000
    elif max_pop >=25:
        N = 5000
    else:
        N = 1000
    days = len(time_series)
    min_rmse = 10000000000
    min_c = 1
    r0,mean_duration,mean_latency = [1,1,1]
    C_values = [4,5,6,7,8,9]
    for C in C_values:        
        infected = time_series
        initial = infected[0]
        removed = 0.01*infected
        def RMSE(p):
            r0,mean_duration,mean_latency = p
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
            sol = solve_ivp(SEIR,[0,days],[N,C*initial,initial,0],t_eval=np.arange(0,days))
            return((sum((sol.y[2]-infected)**2)+ sum((sol.y[3]-removed)**2)**(1/2)))
        msol = minimize(RMSE,[5,10,2],method ='Nelder-Mead')
        error = RMSE(msol.x)
        if error< min_rmse:
            min_rmse = error
            min_c = C
            r0,mean_duration,mean_latency = msol.x
            param = [county,days,N,initial,min_c,r0,mean_duration,mean_latency]
            model_df.loc[i] = param
model_df.to_excel("models/model_weights.xlsx")