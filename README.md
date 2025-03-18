# 0. Intro: Get to know how is the weather in Hong Kong

In this analysis, I want to know more about the weather and seasons of Hong Kong, my new resident city. I will compare to Paris and Seoul (my resident cities for last 15 years(!)) using public data. Which districts of Hong Kong will resemble the most to my previous residencies? (Shall I move to that district to transcend my deepest nostalgia?) How the temperature and sunshine will vary in upcoming months nearby my new apartment? (Since my mom is visiting Hong Kong soon and I don't want to overcook her with the extreme humid heat...)

# 1. Data Sources overview
## 1. Hong Kong weather Data
I used three following datasets available on HK Data Gov web page. 
- Daily maximum temperature data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko)
- Daily mean humidity data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-mean-relative-humidity)
- Daily total railfall data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall)

For each dataset, I had to download one .csv file by district and aggregate 38 files since there's no aggregated file. The data structure was similar for three datasets: 5 columns containing Year, Month, Day, Value (Temperature, Humidity and Rainfall value), and the last column indicating the data completeness. Data Completeness column contains a value of 'C' or '#'. However, the definition of these two values is not found. Nevertheless, we can presume 'C' as 'Complete' and '#' maybe 'Incomplete', as the number of observations having 'C' forms a majority of the dataset - without knowing what 'Incomplete' does mean exactly. Still, when Data Completeness column contains '#', the value is recorded. More troublesome cases are the lines with '\*\*\*' for numerical value column. In my analysis, I have used all values including the ones marked with '#' in Data Completeness column if it contains a value other than '\*\*\*'. 



