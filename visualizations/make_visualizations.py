import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fig, axs = plt.subplots(4, 4,figsize=(16,16))

dataset = pd.read_excel("data/processed/nj_clean.xlsx")
weights = pd.read_excel("models/model_weights.xlsx")
infected_output = pd.read_csv("data/processed/infected_output.csv")
exposed_output = pd.read_csv("data/processed/exposed_output.csv")
for i in range(16):
    county,days,N,initial,min_c,r0,mean_duration,mean_latency = weights.loc[i]
    county = dataset.loc[i].values[0]
    original_infected = dataset.loc[i].values[1:]
    original_infected = original_infected[original_infected>1]
    exposed_out = exposed_output.iloc[i].fillna(0).values
    exposed_out = exposed_out[exposed_out>0]
    infected_out = infected_output.iloc[i].fillna(0).values
    infected_out = infected_out[infected_out>0]
    axs1 = int(i/4)
    axs2 = i%4
    time = np.arange(0,len(infected_out))
    axs[axs1,axs2].plot(time,exposed_out)
    axs[axs1,axs2].plot(time,infected_out)
    axs[axs1,axs2].plot(np.arange(0,days),original_infected,"k*:")
    fig.legend(["Exposed","Infected","Original Infected"])
    title = str(county)+" C="+str(min_c)
    axs[axs1,axs2].set_title(title)
    axs[axs1,axs2].set_xticks([])
    axs[axs1,axs2].set_ylim(0,exposed_out[-1]*1.5)
plt.savefig('visualizations/nj_county_viz.png', bbox_inches='tight')