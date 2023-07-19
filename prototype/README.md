# ML Pipeline Generator Prototype
This is a prototype which generates a kedro pipeline based on user input.

## Usage
Requires Python version 3.10.2

The target kedro project requires package versions described in [requirements.txt](./requirements.txt).

```
python main.py -f file -l loc

file    : YAML file with valid generator input configuration
loc     : kedro project main directory
```

## Interviews
Additionally, copy the dataset [diabetes_prediction_dataset.csv](./data/diabetes_prediction_dataset.csv) and [smoking_history.csv](./data/smoking_history.csv) into the `data/01_raw` directory in the target kedro project.

## Requirements
The requirements listed in [requirements_kedro.txt](requirements_kedro.txt) relate to the kedro project in which the ML pipeline is generated into.
