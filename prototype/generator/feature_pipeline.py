from pathlib import Path

from generator.utils import write_pipeline_file, write_parameters_file


class FeatureEngineering:

    def __init__(self, config: dict, root_dir: Path, feature_pipeline_dir: Path, last_datasets: list) -> None:
        '''
        Params:
        feature_pipeline_dir: path to directory called 'feature_pipeline'
        '''
        self.config = config
        self.root_dir = root_dir
        self.feature_pipeline_dir = feature_pipeline_dir
        self.last_datasets = last_datasets
        self.next_datasets = []
        self.additional_nodes = []
        self.additional_datasets = []
        self._structure()
        self._write_files()
    
    def get_config(self):
        return self.config
    
    def get_additional_nodes(self):
        return self.additional_nodes
    
    def get_additional_datasets(self):
        return self.additional_datasets
    
    def get_next_datasets(self):
        return self.next_datasets
    
    def _structure(self):
        nodes_list = []
        node_jd, dataset_jd = self.Nodes.node_train_test_split(
            self.root_dir,
            self.config,
            [self.last_datasets[0], 'params:split_options']
        )
        self.next_datasets.extend(dataset_jd)
        nodes_list.append(node_jd)
        self.additional_nodes.extend(nodes_list)
        self.config['nodes'].extend(nodes_list)
        #self.config['datasets'].append(dataset_jd)

    def _write_files(self):
        nodes_list = self.additional_nodes
        with open(self.feature_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in nodes_list:
                node_file.write(node['code'])
        write_pipeline_file(self.feature_pipeline_dir, nodes_list)

    class Nodes:
        def node_train_test_split(root_dir: Path, config: dict, input_datasets):
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
            write_parameters_file(root_dir, 'feature_pipeline', params)
            return {
                'func': 'split_train_test',
                'name': 'Train_test_split',
                'code': code,
                'inputs': input_datasets,
                'outputs': ['X_train', 'X_test', 'y_train', 'y_test']
            }, ['X_train', 'X_test', 'y_train', 'y_test']
