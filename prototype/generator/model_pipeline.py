from pathlib import Path

from .utils import write_parameters_file, write_pipeline_file, dataset_wrapper


class ModelPipeline:

    def __init__(self, config: dict, root_dir: Path, model_pipeline_dir: Path, first_dataset: str) -> None:
        self.name = 'model_pipeline'
        self.config = config
        self.root_dir = root_dir
        self.model_pipeline_dir = model_pipeline_dir
        self.first_dataset = first_dataset
        self.next_datasets = []
        self.additional_nodes = []
        self.params = {}
        self._structure()
        self._write_files()

    def get_config(self):
        return self.config
    
    def get_next_datasets(self):
        return self.next_datasets
    
    def _structure(self):
        nodes_list = []
        # Add train-test split node
        node_tts, dataset_tts, params = self.Nodes.node_train_test_split(
            self.root_dir, self.config, self.config['additional']['feature_all_names'], input_dataset=self.first_dataset
        )
        nodes_list.append(node_tts)
        self.next_datasets.extend(dataset_tts)
        self.params.update(params)
        # Add normalization nodes
        scaled = False
        if len(self.config['additional']['scaled_feature_names']) > 0:
            nodes, dataset_sf = self.Nodes.node_scale_features(self.root_dir, self.config['additional']['scaled_feature_names'])
            nodes_list.extend(nodes)
            self.next_datasets.extend(dataset_sf)
            scaled = True
        # Add training node
        node_mt, dataset_mt, params = self.Nodes.node_training_model(self.root_dir, self.config, scaled)
        nodes_list.append(node_mt)
        self.next_datasets.extend(dataset_mt)
        self.params.update(params)
        # Add evaluation node
        node_me = self.Nodes.node_model_evaluation(self.root_dir, self.config, scaled)
        nodes_list.append(node_me)
        # Collect additional nodes
        self.additional_nodes.extend(nodes_list)

    def _write_files(self):
        nodes_list = self.additional_nodes
        # write nodes.py
        with open(self.model_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in nodes_list:
                node_file.write(node['code'])
        # write pipeline.py
        write_pipeline_file(self.model_pipeline_dir, nodes_list)
        # write pipeline specific params
        write_parameters_file(self.root_dir, self.name, self.params)

    class Nodes:
        def node_train_test_split(root_dir: Path, config: dict, feature_names: list, input_dataset: list):
            code = f'''import pandas as pd
import numpy as np
from typing import Dict, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
            
def split_train_test(data: pd.DataFrame, parameters: Dict) -> Tuple:
    # Encode features which are not numeric
    data[data.select_dtypes(exclude=np.number).columns] = OrdinalEncoder().fit_transform(data.select_dtypes(exclude=np.number))
    # Create X and y
    target_label = parameters['target_label']
    y = data[target_label]
    if len(parameters['features']) == 0:
        X = data.drop(target_label, axis=1)
    else:
        feature_params = parameters['features']
        X = data[feature_params]
    train_ratio = parameters.get('train-test-split', {{}}).get('train-ratio', None)
    test_ratio = parameters.get('train-test-split', {{}}).get('test-ratio', None)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=train_ratio,
        test_size=test_ratio,
        {'stratify=y' if config['problem'].lower() == 'classification' else ''}
    )
    return X_train, X_test, y_train, y_test
'''
            params = {'split_options': {
                'train-test-split': config['train-test-split'],
                'features': feature_names,
                'target_label': config['target_label'],},
                }
            return {
                'func': 'split_train_test',
                'name': 'Train_test_split',
                'code': code,
                'inputs': [input_dataset, 'params:split_options'],
                'outputs': ['X_train', 'X_test', 'y_train', 'y_test']
            }, [
                dataset_wrapper('X_train', 'memory', layer='feature'),
                dataset_wrapper('X_test', 'memory', layer='feature'),
                dataset_wrapper('y_train', 'memory', layer='feature'),
                dataset_wrapper('y_test', 'memory', layer='feature')
            ], params

        def node_training_model(root_dir: str, config: dict, scaled: bool=False):
            code = f'''import pandas as pd
from sklearn.base import BaseEstimator


def train_model(X_train: pd.DataFrame, y_train: pd.Series, model_options: dict, metrics: list):
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV
    from mlflow.sklearn import autolog

    class DummyEstimator(BaseEstimator):
        def fit(self): pass
        def score(self): pass
    
    autolog()
    pipeline = Pipeline([('clf', DummyEstimator())])
    search_space = []
    for param in model_options:
        new_model = {{'clf': [get_model_type(param['algorithm'])()]}}
        if param.get('parameters', None):
            new_model.update({{'clf__'+key: value for key, value in param['parameters'].items()}})
        search_space.append(new_model)
    grid_search = GridSearchCV(
        pipeline,
        search_space,
        scoring=metrics,
        refit=metrics[0],
        verbose=4)
    grid_search.fit(X_train, y_train)
    return [grid_search.best_estimator_]
    

def get_model_type(type: str):
    from sklearn import tree, linear_model
    model_types = {{
        'tree.DecisionTreeClassifier': tree.DecisionTreeClassifier,
        'tree.DecisionTreeRegressor': tree.DecisionTreeRegressor,
        'linear_model.LinearRegression': linear_model.LinearRegression,
        'linear_model.LogisticRegression': linear_model.LogisticRegression,
        'linear_model.PassiveAggressiveClassifier': linear_model.PassiveAggressiveClassifier,
        'linear_model.RidgeClassifier': linear_model.RidgeClassifier,
        'linear_model.SGDClassifier': linear_model.SGDClassifier,
        'linear_model.Ridge': linear_model.Ridge,
    }}
    return model_types.get(type)
'''
            models = []
            for m in config['training']['models']:
                params = m.get('parameters', None)
                new_model = {'algorithm': m['algorithm']}
                if params:
                    new_model['parameters'] = params
                models.append(new_model)
            metric_params = config.get('metrics') if config.get('metrics') else ''
            parameters = {'model_options': models, 'metrics': metric_params}
            model_name = 'Model'
            output_dataset = dataset_wrapper(
                name=model_name, type='pickle', filepath=f'data/06_models/{model_name}.pickle', layer='model')
            X_train_input_name = 'X_train_scaled' if scaled else 'X_train'
            return {
                'func': 'train_model',
                'name': 'Model_Training',
                'code': code,
                'inputs': [X_train_input_name, 'y_train', 'params:model_options', 'params:metrics'],
                'outputs': [model_name]
            }, [output_dataset], parameters

        def node_model_evaluation(root_dir: str, config: dict, scaled: bool=False):
            mixin = 'RegressorMixin' if str(config['problem']).lower() == 'regression' else 'ClassifierMixin'
            model_type = 'regressor' if str(config['problem']).lower() == 'regression' else 'classifier'
            default_metric = 'r2' if str(config['problem']).lower() == 'regression' else 'accuracy'
            code = f'''
from sklearn.base import {mixin}
from sklearn.metrics import get_scorer
from mlflow import log_metric, evaluate
from mlflow.sklearn import log_model
def evaluate_model(model: {mixin}, X_test: pd.DataFrame, y_test: pd.Series, metrics: list):
    if not hasattr(model, 'predict'):
        raise AttributeError('The model has no attribute "predict".')
    model_info = log_model(model, 'model')
    data = X_test.join(y_test)
    evaluate(model_info.model_uri, data, targets=y_test.name, model_type='{model_type}')
    if len(metrics) == 0:
        score = model.score(X_test, y_test)
        log_metric('{default_metric}', score)
        return
    for metric in metrics:
        score = get_scorer(metric)(model, X_test, y_test)
        log_metric(metric, score)

    '''
            X_test_input_name = 'X_test_scaled' if scaled else 'X_test'
            return {
                'func': 'evaluate_model',
                'name': 'Model_Evaluation',
                'code': code,
                'inputs': ['Model', X_test_input_name, 'y_test', 'params:metrics'],
                'outputs': None
            }

        def node_scale_features(root_dir: str, feature_names: dict):
            feature_names_str = ','.join("'{0}'".format(x) for x in feature_names)
            code_X_train = f'''
from sklearn.preprocessing import MinMaxScaler
def scale_X_train(X_train: pd.DataFrame):
    scaler = MinMaxScaler()
    X_train[[{feature_names_str}]] = scaler.fit_transform(X_train[[{feature_names_str}]])
    return X_train, scaler
'''
            code_X_test = f'''
def scale_X_test(X_test: pd.DataFrame, scaler):
    X_test[[{feature_names_str}]] = scaler.transform(X_test[[{feature_names_str}]])
    return [X_test]
'''
            return [{
                'func': 'scale_X_train',
                'name': 'Scale_X_train',
                'code': code_X_train,
                'inputs': ['X_train'],
                'outputs': ['X_train_scaled', 'scaler']
            }, {
                'func': 'scale_X_test',
                'name': 'Scale_X_test',
                'code': code_X_test,
                'inputs': ['X_test', 'scaler'],
                'outputs': ['X_test_scaled']
            }], [
                dataset_wrapper('X_train_scaled', 'memory', layer='model_input'),
                dataset_wrapper('X_test_scaled', 'memory', layer='model_input')
            ]
