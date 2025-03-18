
import pandas as pd
import time
import datetime
import os
import glob

# Public Data Downloaded from HK Data Gov website:
# https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko

# CSV File list in 0_Data directory:
list_files = glob.glob("0_Data/*.csv")

# Aggregated Data templete:
Agg_Data = pd.DataFrame()
#columns = ['Date','year','Temp','Flag']
for Data_by_dist in list_files:
    
    Max_region=pd.read_csv(Data_by_dist, 
                       sep=",", skiprows=3, header = None)

    LMMAXT_HKP_ = pd.DataFrame(Max_region)
    LMMAXT_HKP_.columns = ['year', 'month', 'day', 'Temp', 'Flag']

    ## Data Filter ##
    # F1: Delete the last 3 lines:
    LMMAXT_HKP_ = LMMAXT_HKP_.iloc[:-3]

    LMMAXT_HKP_['month'] = LMMAXT_HKP_['month'].astype(int)
    LMMAXT_HKP_['day'] = LMMAXT_HKP_['day'].astype(int)
    LMMAXT_HKP_ = LMMAXT_HKP_.loc[LMMAXT_HKP_['Temp']!="***"]
    LMMAXT_HKP_['Temp'] = LMMAXT_HKP_['Temp'].astype(float)

    # F2: Delete data of 2007 since incomplete (only from october)
    LMMAXT_HKP_ = LMMAXT_HKP_.loc[LMMAXT_HKP_['year']!='2007']

    # Date parsing 
    LMMAXT_HKP_date = pd.to_datetime(LMMAXT_HKP_[['year','month', 'day']])
    #LMMAXT_HKP_date = LMMAXT_HKP_date.dt.dayofyear

    # Concatenate parsed date + Table 
    LMMAXT_HKP_2 = pd.concat([LMMAXT_HKP_date, LMMAXT_HKP_[['year','Temp', 'Flag']]],
            axis = 1)
    LMMAXT_HKP_2 = LMMAXT_HKP_2.rename(columns = {0: "Date"})
    
    # Observatory center name
    LMMAXT_HKP_2['Dist'] = Data_by_dist.split("Data/")[1].split("_")[1]
    LMMAXT_HKP_2['NObs_Dist'] = LMMAXT_HKP_2.shape[0]
    
    Agg_Data = pd.concat([Agg_Data, LMMAXT_HKP_2], axis = 0, ignore_index=True)


# Plot : Max temperature measured at HKP

# (1) Monthly Average Max temperature

LMMAXT_HKP_monthlyMean = LMMAXT_HKP_.groupby(['year', 'month'])['Temp'].mean()
LMMAXT_HKP_monthlyMean = pd.DataFrame(LMMAXT_HKP_monthlyMean.reset_index())

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="dark")

# Plot each year's time series in its own facet
g = sns.relplot(
    data=LMMAXT_HKP_monthlyMean,
    x="month", y="Temp", col="year", hue="year",
    kind="line", palette="crest", linewidth=2, zorder=5,
    col_wrap=3, height=2, aspect=1.5, legend=False,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    sns.lineplot(
        data=LMMAXT_HKP_monthlyMean, x="month", y="Temp", units="year",
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

# Reduce the frequency of the x axis ticks
ax.set_xticks(ax.get_xticks()[::2])

# Tweak the supporting aspects of the plot
g.set_titles("")
g.set_axis_labels("", "")
g.tight_layout()
plt.show()