# 0. Intro: Get to know how is the weather in Hong Kong

In this analysis, I want to know more about the weather and seasons of Hong Kong, my new resident city. I will compare to Paris (my resident city for last 10 years(!)) using public data. How exactly the weather is different here? How the temperature and sunshine will vary in upcoming months nearby my new apartment? (Since my mom is visiting Hong Kong soon and I don't want to overcook her with the extreme humid heat...)

# 1. Overview of data sources
## a. Hong Kong weather data
I used three following datasets available on HK Data Gov web page. 
- Daily maximum temperature data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko)
- Daily mean humidity data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-mean-relative-humidity)
- Daily total railfall data (https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall)

For each dataset, I had to download one .csv file by district (weather observatory) and aggregate **38 files** since there's no aggregated file. The data structure was similar for three datasets: 5 columns containing **Year, Month, Day, Value (Temperature, Humidity and Rainfall value)**, and the last column indicating the **data completeness**. After a review, Data Completeness column contains a value of 'C' or '#'. However, the definition of these two values is not found. Nevertheless, we can presume 'C' as 'Complete' and '#' maybe 'Incomplete', as the number of observations having 'C' forms a majority of the dataset - without knowing what 'Incomplete' does mean exactly. Still, when Data Completeness column contains '#', the value is sometimes recorded. More troublesome cases are the lines with '\*\*\*' for numerical value column. This differs for three datasets as well. For the temperature dataset, the # flag includes some numerical values and some \*\*\* values, while \*\*\* values are always flagged to #. For the humidity data, # flagged values always contain a numerical value. A complemetary set of data contains \*\*\* values, unflagged to #. 

Without access to the definition of these flags, I have used all numerical values including the ones flagged to '#' in Data Completeness column if it contains a normal numerical value other than '\*\*\*'. 

As of Temperature dataset, the percentage of observations filled with '\*\*\*' takes less than 1% for 71% of 38 Hong Kong districts. It is 5.5% at maximum, for Ngong Ping district observatory (NGP).

## b. Paris weather data

For Paris weather data, I used the data available on the website of France Data Gouv (https://www.data.gouv.fr/fr/datasets/donnees-climatologiques-de-base-quotidiennes/).

The format of the daily weather data for France is a set of two CSV files by department and for a certain period. For example, I have 2 CSV files for Paris department (75) for the period of 1950-2023, one file for the essential parameters (Temperature, Rainfall, etc.) and the other one for the complements (Humidity is included in this file). I have another 2 CSV files for the period of last two years (2023-2024).

Since the three variables that I want to analyze to compare with HK weather information are Temperature, Humidity and Rainfall, I used these 4 files representing the weather data of Paris.

And to have only one value representing the global weather parameter for Paris, I choose to average these values over observatories.  
