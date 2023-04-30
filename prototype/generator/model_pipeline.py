from pathlib import Path

from .utils import write_parameters_file, write_pipeline_file, dataset_wrapper


class ModelPipeline:

    def __init__(self, config: dict, root_dir: Path, model_pipeline_dir: Path, last_datasets: list) -> None:
        self.name = 'model_pipeline'
        self.config = config
        self.root_dir = root_dir
        self.model_pipeline_dir = model_pipeline_dir
        self.last_datasets = last_datasets
        self.next_datasets = []
        self.additional_nodes = []
        self._structure()
        self._write_files()

    def get_config(self):
        return self.config
    
    def get_next_datasets(self):
        return self.next_datasets
    
    def _structure(self):
        nodes_list = []
        # Add train-test split node
        node_tts, dataset_tts = self.Nodes.node_train_test_split(
            self.root_dir, self.name, self.config, input_datasets=[self.last_datasets[0], 'params:split_options']
        )
        nodes_list.append(node_tts)
        # Add normalization nodes
        # Add training node
        node_mt, dataset_mt = self.Nodes.node_training_model(self.root_dir, self.name, self.config)
        nodes_list.append(node_mt)
        self.next_datasets.extend(dataset_mt)
        # Add evaluation node
        node_me = self.Nodes.node_model_evaluation(self.root_dir, self.name, self.config)
        nodes_list.append(node_me)
        # Collect additional nodes
        self.additional_nodes.extend(nodes_list)
        self.config['nodes'].extend(nodes_list)

    def _write_files(self):
        nodes_list = self.additional_nodes
        with open(self.model_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in nodes_list:
                node_file.write(node['code'])
        write_pipeline_file(self.model_pipeline_dir, nodes_list)

    class Nodes:
        def node_train_test_split(root_dir: Path, name: str, config: dict, input_datasets):
            code = f'''import pandas as pd
from typing import Dict, Tuple
from sklearn.model_selection import train_test_split
            
def split_train_test(data: pd.DataFrame, parameters: Dict) -> Tuple:
    training_params = parameters['training']
    X = data[training_params['features']]
    y = data[training_params['target_label']]
    train_ratio = parameters.get('train-test-split', None).get('train-ratio', None)
    test_ratio = parameters.get('train-test-split', None).get('test-ratio', None)
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
                'training': {'features': config['training']['features'],
                             'target_label': config['training']['target_label']}
                }}
            write_parameters_file(root_dir, name, params)
            return {
                'func': 'split_train_test',
                'name': 'Train_test_split',
                'code': code,
                'inputs': input_datasets,
                'outputs': ['X_train', 'X_test', 'y_train', 'y_test']
            }, ['X_train', 'X_test', 'y_train', 'y_test']

        def node_training_model(root_dir: str, name: str, config: dict):
            code = '''import pandas as pd
from sklearn.base import BaseEstimator


def train_model(X_train: pd.DataFrame, y_train: pd.Series, parameters):
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV
    from mlflow import log_params

    class DummyEstimator(BaseEstimator):
        def fit(self): pass
        def score(self): pass
    
    pipeline = Pipeline([('clf', DummyEstimator())])
    search_space = []
    for param in parameters:
        new_model = {'clf': [get_model_type(param['algorithm'])()]}
        if not param.get('parameters', None) is None:
            new_model.update({'clf__'+key: value for key, value in param['parameters'].items()})
        search_space.append(new_model)
    grid_search = GridSearchCV(pipeline, search_space, verbose=4)
    grid_search.fit(X_train, y_train)
    log_params({'best_params': grid_search.best_params_})
    return [grid_search.best_estimator_]
    

def get_model_type(type: str):
    from sklearn import tree, linear_model
    model_types = {
        'tree.DecisionTreeClassifier': tree.DecisionTreeClassifier,
        'tree.DecisionTreeRegressor': tree.DecisionTreeRegressor,
        'linear_model.LinearRegression': linear_model.LinearRegression,
    }
    return model_types.get(type)
'''
            models = []
            for m in config['training']['models']:
                params = m.get('parameters', None)
                new_model = {'algorithm': m['algorithm']}
                if not params is None:
                    new_model['parameters'] = params
                models.append(new_model)
            write_parameters_file(root_dir, name, {'model_options': models})
            model_name = 'Model'
            output_dataset = dataset_wrapper(model_name, 'pickle', f'data/06_models/{model_name}.pickle', versioned=True)
            return {
                'func': 'train_model',
                'name': 'Model_Training',
                'code': code,
                'inputs': ['X_train', 'y_train', 'params:model_options'],
                'outputs': [model_name]
            }, [output_dataset]

        def node_model_evaluation(root_dir: str, name: str, config: dict):
            mixin = 'RegressorMixin' if str(config['problem']).lower() == 'regression' else 'ClassifierMixin'
            metric = 'R2' if str(config['problem']).lower() == 'regression' else 'Accuracy'
            code = f'''
from sklearn.base import {mixin}
from mlflow import log_metric
def evaluate_model(model: {mixin}, X_test: pd.DataFrame, y_test: pd.Series):
    result = model.score(X_test, y_test)
    log_metric('{metric}', result)

    '''
            return {
                'func': 'evaluate_model',
                'name': 'Model_Evaluation',
                'code': code,
                'inputs': ['Model', 'X_test', 'y_test'],
                'outputs': None
            }
