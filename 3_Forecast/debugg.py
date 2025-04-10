import sys
sys.path.append('/Users/nayeongkim/Desktop/HKweather/')
print(sys.path)
import pandas as pd
from functions.eval import evaluate_performance
from functions import ts_utils
import datetime

daily_temp_train = pd.read_parquet("../0_Data/wrangled/daily_temp_train.parquet")
daily_temp_val = pd.read_parquet("../0_Data/wrangled/daily_temp_val.parquet")
daily_temp_test = pd.read_parquet("../0_Data/wrangled/daily_temp_test.parquet")
# Data Frequency setting
freq = "D" # daily frequency (not even the business day frequency)
daily_temp_train.reset_index(inplace = True)
daily_temp_test.reset_index(inplace = True)
daily_temp_val.reset_index(inplace = True)
pred_df = pd.concat([daily_temp_train, daily_temp_val])
print(len(set(pred_df['index_n'])))
print(pred_df.shape[0])
from statsforecast import StatsForecast
from utilsforecast.evaluation import evaluate
from statsforecast.models import (
    Naive,
    SeasonalNaive,
    HistoricAverage,
    WindowAverage,
    SeasonalWindowAverage,
    RandomWalkWithDrift,
    HoltWinters,
    #ETS,
    AutoETS,
    AutoARIMA,
    ARIMA,
    AutoTheta,
    DynamicTheta,
    DynamicOptimizedTheta,
    Theta,
    OptimizedTheta,
    TBATS,
    AutoTBATS,
    MSTL
)
from functions.ts_utils import mase, mae, mse, forecast_bias


ts_train=daily_temp_train
ts_test=daily_temp_val 
models=[Naive()]
metrics=[mase, mae, mse, forecast_bias]
freq=freq
level=[]  # Ensure this is correct or adjust as necessary
id_col='index_n'
time_col='Date'
target_col='TX'
h=len(daily_temp_val)
metric_df=metrics  # Pass None or an existing DataFrame if you want to append results

results = ts_test.copy()

# Timing dictionary to store train and predict durations
timing = {}

for model in models:
    model_name = model.__class__.__name__
evaluation = {}  # Reset the evaluation dictionary for each model

# Start the timer for fitting and prediction
start_time = datetime.datetime.now()

# Instantiate StatsForecast class
sf = StatsForecast(
    models=[model],
    freq=freq,
    n_jobs=-1,
    #fallback_model=Naive()
)

print(sf)

# Efficiently predict without storing memory
y_pred = sf.forecast(
    h=h,
    df=ts_train,
    #target_col=target_col,
    fitted = True
)

print(y_pred)