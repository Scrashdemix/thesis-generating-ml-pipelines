# Specification
This is the specification of the configuration yaml file.
## Datasets
```
datasets:
  - name: <name>
    type: 'csv' | 'json' | 'xls' | 'parquet'
    filepath: <path to file/remote>
    # [Optional:]
    load_args:
      <Arguments according to kedro's specification>
    save_args:
      <Arguments according to kedro's specification>
    credentials:
      <Credentials needed for accessing the dataset>
  - name: ...
    ...
```
## Visualization
```
visualization: true  # [Optional:] data visualization using sweetviz (html report gets generated in data/08_reporting)
```
## Problem Type
```
problem: 'regression' | 'classification'  # Type of problem
```
## Target Label
```
target_label: <name of the feature which should be used as target variable>
```
## Train-Test Split
```
train-test-split:
  train-ratio: <Value between 0 and 1>  # [Optional: ] Ratio of training data from the original data
  test-ratio: <Value between 0 and 1>  # [Optional: ] Ratio of test data from the original data
```
## Feature Selection & Engineering
```
features:  # [Optional:] list of feature names which are used for training all models. If none, all available features are used
    - <name of feature>:
        scaled: true  # [Optional:] whether this feature shall be scaled using scikit-learn's MinMaxScaler
        cut_outliers: percentile | iqr | zscore  # [Optional:] whether outliers will be dropped from the dataframe. The value determines the algorithm chosen for detecting outliers. 'percentile' removes the 5th and 95th percentile of the data, 'iqr' removes data points which are outside of 1.5-times the interquartile range below/above the 1st and 3rd quartile, 'zscore' removes data points with a z-score above 3 
    - ...
```
## Model Training
```
training:
  models:
    - algorithm: <model algorithm>  # maybe some kind of key for sklearn (Example: 'linear_model.LinearRegression')
      parameters:
        <name of parameter>:  # List of values or min/max
```
## Model Evaluation
```
metrics: <string id / list of string ids> 
# String id or list of those of the corresponding sklearn metric
```