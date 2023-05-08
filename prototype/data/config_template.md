This is the specification of the configuration yaml file.
```
datasets:
  - name: <name>
    type: 'csv' | ...
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
visualization: 'sweetviz'  # [Optional:] data visualization using sweetviz (html report gets generated)
problem: 'regression' | 'classification'  # Type of problem
train-test-split:
  train-ratio: <Value between 0 and 1>  # Ratio of training data from the original data
  test-ratio: <Value between 0 and 1>  # Ratio of test data from the original data
features:  # [Optional:] list of feature names which are used for training all models. If none, all available features are used
    - <name of feature>:
        normalized: MinMaxScaler  # [Optional:] whether this feature shall be normalized using this scikit-learn scaler
    - ...
target_label: <name of the feature which should be used as target variable>
training:
  models:
    - algorithm: <model algorithm>  # maybe some kind of key for sklearn
      cv: <int> | false  # Cross-validation's k if it's enabled, default: false
      parameters:
        <name of parameter>:  # List of values or min/max
metrics: <string id / list of string ids>  # String id or list of those of the corresponding sklearn metric

```