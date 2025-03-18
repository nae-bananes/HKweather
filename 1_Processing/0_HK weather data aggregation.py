
import pandas as pd
import time
import datetime
import os
import glob

# Public Data Downloaded from HK Data Gov website:
# https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko

# CSV File list in 0_Data directory:
list_files = glob.glob("0_Data/*.csv")
len(list_files)   
# Aggregated Data templete:
Agg_Data = pd.DataFrame()
Data_summary = pd.DataFrame()

for Data_by_dist in list_files:
    
    Max_region=pd.read_csv(Data_by_dist, 
                       sep=",", skiprows=3, header = None)

    LMMAXT_HKP_ = pd.DataFrame(Max_region)
    LMMAXT_HKP_.columns = ['year', 'month', 'day', 'value', 'Flag']

    # Data Quality indicators:
    Obs_summary = pd.DataFrame({'Dist': [Data_by_dist.split("Data/")[1].split("_")[1]],
                                'NObs_Dist': [LMMAXT_HKP_.shape[0]],
                                'NObs_Flagged': [LMMAXT_HKP_.loc[LMMAXT_HKP_['Flag']=="#"].shape[0]],
                                'NObs_Starred': [LMMAXT_HKP_.loc[LMMAXT_HKP_['value']=="***"].shape[0]],
                                'NObs_Str_Shrp': [LMMAXT_HKP_.loc[(LMMAXT_HKP_['value']=="***")&(LMMAXT_HKP_['Flag']=="#")].shape[0]]})
   
    Obs_summary['Purge_Pct'] = round(100*Obs_summary['NObs_Starred']/Obs_summary['NObs_Dist'],2)
    Data_summary = pd.concat([Data_summary, Obs_summary], axis = 0)
    
    ## Data Filter ##
    # F1: Delete the last 3 lines:
    LMMAXT_HKP_ = LMMAXT_HKP_.iloc[:-3]

    LMMAXT_HKP_['month'] = LMMAXT_HKP_['month'].astype(int)
    LMMAXT_HKP_['day'] = LMMAXT_HKP_['day'].astype(int)
    LMMAXT_HKP_ = LMMAXT_HKP_.loc[LMMAXT_HKP_['value']!="***"]
    LMMAXT_HKP_['value'] = LMMAXT_HKP_['value'].astype(float)

    # F2: Delete data of 2007 since incomplete (only from october)
    LMMAXT_HKP_ = LMMAXT_HKP_.loc[LMMAXT_HKP_['year']!='2007']

    # Date parsing 
    LMMAXT_HKP_date = pd.to_datetime(LMMAXT_HKP_[['year','month', 'day']])
    #LMMAXT_HKP_date = LMMAXT_HKP_date.dt.dayofyear

    # Concatenate parsed date + Table 
    LMMAXT_HKP_2 = pd.concat([LMMAXT_HKP_date, LMMAXT_HKP_[['year','value', 'Flag']]],
            axis = 1)
    LMMAXT_HKP_2 = LMMAXT_HKP_2.rename(columns = {0: "Date"})
    
    Agg_Data = pd.concat([Agg_Data, LMMAXT_HKP_2], axis = 0, ignore_index=True)


Data_summary.loc[Data_summary['Purge_Pct']<1].shape[0]/Data_summary.shape[0]

treated_data_rep = r'0_Data/wrangled/' 
if not os.path.exists(treated_data_rep):
    os.makedirs(treated_data_rep)
Agg_Data.to_pickle(treated_data_rep+"Agg_Data.pkl")
