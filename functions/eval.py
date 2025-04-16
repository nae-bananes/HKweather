

def evaluate_performance(ts_train, ts_test, models, metrics, 
                         freq, level, id_col, time_col, target_col, h, metric_df=None):
    
    import datetime
    import pandas as pd
    from statsforecast import StatsForecast
    from statsforecast.models import (    
    Naive,
    SeasonalNaive,
    HistoricAverage,
    WindowAverage,
    SeasonalWindowAverage,
    RandomWalkWithDrift,
    HoltWinters,
    ETS,
    AutoETS,
    AutoARIMA,
    #ARIMA,
    AutoTheta,
    DynamicTheta,
    DynamicOptimizedTheta,
    Theta,
    OptimizedTheta,
    #TBATS,
    #AutoTBATS,
    MSTL
    )

    if metric_df is None:
        metric_df = pd.DataFrame()  # Initialize an empty DataFrame if not provided

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
            fallback_model=Naive()
        )

        # Efficiently predict without storing memory
        y_pred = sf.forecast(
            h=h,
            df=ts_train,
            #id_col=id_col,
            #time_col=time_col,
            #target_col=target_col,
            #level=level,
            fitted =True
        )

        # Calculating the duration
        duration = datetime.datetime.now() - start_time
        timing[model_name] = duration

        # Merge prediction results to the original dataframe
        results = results.merge(y_pred, how='left', on=[id_col, time_col])

        ids = ts_train[id_col].unique()

        # Calculate metrics
        for id in ids:

            temp_results = results[results[id_col] == id]
            temp_train = ts_train[ts_train[id_col] == id]

            for metric in metrics:
                metric_name = metric.__name__
                if metric_name == 'mase':
                    evaluation[metric_name] = metric(temp_results[target_col].values,
                                                    temp_results[model_name].values,
                                                    temp_train[target_col].values)
                else:
                    evaluation[metric_name] = metric(temp_results[target_col].values, temp_results[model_name].values)
            evaluation[id_col] = id
            evaluation['Time Elapsed'] = timing[model_name]

            # Prepare and append this model's results to metric_df
            temp_df = pd.DataFrame(evaluation, index=[0])
            temp_df['Model'] = model_name
            metric_df = pd.concat([metric_df, temp_df], ignore_index=True)


    return results, metric_df