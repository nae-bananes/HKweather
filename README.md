# 0. Intro: Get to know how is the weather in Hong Kong

In this analysis, I want to know more about the weather and seasons of Hong Kong, my new resident city. I will compare to Paris and Seoul (my resident cities for last 15 years(!)) using public data. Which districts of Hong Kong will resemble the most to my previous residencies? (Shall I move to that district to transcend my deepest nostalgia?) How the temperature and sunshine will vary in upcoming months nearby my new apartment? (Since my mom is visiting Hong Kong soon and I don't want to overcook her with the extreme humid heat...)

# 1. Overview of data sources
## a. Hong Kong weather Data
I used three following datasets available on HK Data Gov web page. 
- Daily maximum temperature data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko)
- Daily mean humidity data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-mean-relative-humidity)
- Daily total railfall data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall)

For each dataset, I had to download one .csv file by district (weather observatory) and aggregate **38 files** since there's no aggregated file. The data structure was similar for three datasets: 5 columns containing **Year, Month, Day, Value (Temperature, Humidity and Rainfall value)**, and the last column indicating the **data completeness**. After a review, Data Completeness column contains a value of 'C' or '#'. However, the definition of these two values is not found. Nevertheless, we can presume 'C' as 'Complete' and '#' maybe 'Incomplete', as the number of observations having 'C' forms a majority of the dataset - without knowing what 'Incomplete' does mean exactly. Still, when Data Completeness column contains '#', the value is sometimes recorded. More troublesome cases are the lines with '\*\*\*' for numerical value column. This differs for three datasets as well. For the temperature dataset, the # flag includes some numerical values and some \*\*\* values, while \*\*\* values are always flagged to #. For the humidity data, # flagged values always contain a numerical value. A complemetary set of data contains \*\*\* values, unflagged to #. 

Without access to a definition of these flags, I have used all numerical values including the ones flagged to '#' in Data Completeness column if it contains a normal numerical value other than '\*\*\*'. 

As of Temperature dataset, the percentage of observations filled with '\*\*\*' takes less than 1% for 72% of 38 Hong Kong districts. It is 5.5% at maximum, for Ngong Ping district observatory (NGP).



