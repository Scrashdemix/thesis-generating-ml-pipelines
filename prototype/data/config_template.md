This is the specification of the configuration yaml file.
```
datasets:
  - name: <name>
    type: 'csv' | ...
    filepath: <path to file/remote>
    # [Optional:]
    versioned: true | false  # default: false
    load_args:
      <Arguments according to kedro's specification>
    save_args:
      <Arguments according to kedro's specification>
    credentials:
      <Credentials needed for accessing the dataset>
  - name: ...
    ...
problem: 'regression' | 'classification'  # Type of problem
train-test-split:
  train-ratio: <Value between 0 and 1>  # Ratio of training data from the original data
training:
  features:  # [Optional:] list of feature names which are used for training all models. If none, all available features are used
    - <name of feature>
    - ...
  models:
    - algorithm: <model algorithm>  # maybe some kind of key for sklearn
      cv: <int> | false  # Cross-validation's k if it's enabled default: false
      parameters:
        <name of parameter>:  # List of values or min/max

```