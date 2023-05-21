# Interview Round 2
This is the questionnaire for the second round of interviews.

## Introduction
The introduction of the prototype to the participant contains a short description of how the input of the generator should look like and how the generator can be executed as well as a short guide on installation.

## Experience Questions
- __Experience with kedro__: Years of professional experience
- __Experience with MLflow__: Years of professional experience

If the participant has no experience with kedro, the interviewer will explain the folder and file structure as well as kedro-viz.

If the participant has no experience with MLflow, the interviewer will explain the basic functionality using the MLflow UI.

## Exercise
After the installation process, the participant is able to experiment and play around with different input for the generator and use the resulting ML pipelines for 10 minutes.

In the following 20 minutes the participant is tasked with solving an exercise using the generator. This exercise consists of a classification task using a [diabetes prediction dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset). This dataset is split in two separate datasets to be able to show the functionality of the generator to add the functionality to join datasets to the generated pipeline. The goal of the exercise is to build a pipeline with min-max scaling as well as outlier detection and removal.

The time needed for solving the task is measured.

## Quantitative Questions
The participant can rate the extend to which they agree with the statement on a seven-level scale (Extremely likely, quite likely, slightly likely, neither, slightly unlikely, quite unlikely, extremely unlikely).
### Usefulness
- __Work More Quickly__: Using the generator in my job would enable me to accomplish tasks more quickly.
- __Job Performance__: Using the generator would improve my job performance.
- __Increase Productivity__: Using the generator in my job would increase my productivity.
- __Effectiveness__: Using the generator would enhance my effectiveness on the job.
- __Makes Job Easier__: Using the generator would make it easier to do my job.
- __Overall Usefulness__: I would find the generator useful in my job.

### Ease of Use
- __Ease of Learning__: Learning to operate the generator would be easy for me.
- __Controllable__: I would find it easy for me to get the generator to do what i want to do.
- __Understandable__: My interaction with the generator would be clear and understandable.
- __Flexible__: I would find the generator to be flexible to interact with.
- __Effort to Become Skillful__: It would be easy for me to become skillful at using the generator.
- __Overall Ease of Use__: I would find the generator easy to use.

## Qualitative Questions
- How can the generator be improved?
  - __Interaction__:
    - User input
      - How can the user input be improved?
      - What kind of user input/user interaction would you prefer?
    - Program execution
      - How would you like to start the generation process?
      - What output format/kind do you prefer? (Current: Existing kedro project is modified)
  - __Resulting pipeline__:
    - Pipeline structure
      - What do you think about the structure of the resulting pipeline?
      - How would you improve the structure of the resulting pipeline?
    - Support for data engineering algorithms
      - How can the existing data engineering algorithms can be improved?
      - What data engineering algorithms would you want to be added? 
    - Support for feature engineering algorithms
      - How can the existing feature engineering algorithms can be improved?
      - What feature engineering algorithms would you want to be added?
    - More general AutoML
      - What do you think about AutoML as part of the resulting pipeline?
      - Would you use an AutoML functionality?
    - Model Deployment Pipeline
      - How important would be a generated model deployment pipeline for you?
      - What functionality could be part of a model deployment pipeline?
    - Tool & platform support besides kedro & MLflow
      - Which platforms would you like being supported?
      - Which tools would you like being supported?
