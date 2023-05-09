from pathlib import Path
from generator.utils import write_pipeline_file, dataset_wrapper


class DataPipeline:

    def __init__(self, config: dict, data_pipeline_dir: Path) -> None:
        '''
        Params:
        data_pipeline_dir: path to directory called 'data_pipeline'
        '''
        self.config = config
        self.data_pipeline_dir = data_pipeline_dir
        self.additional_datasets = []
        self.next_datasets = []  # names of datasets for next pipelines
        self._structure()
        self._write_files()

    def get_config(self):
        return self.config
    
    def get_additional_datasets(self):
        return self.additional_datasets
    
    def get_next_datasets(self):
        return self.next_datasets
    
    def _structure(self):
        nodes_list = []
        node_jd, dataset_jd = self.Nodes.node_join_datasets(dataset_names=[ds['name'] for ds in self.config['datasets']])
        nodes_list.append(node_jd)
        self.config['nodes'].extend(nodes_list)
        self.config['datasets'].append(dataset_jd)
        self.next_datasets.append(dataset_jd['name'])
    
    def _write_files(self):
        nodes_list = self.config['nodes']
        with open(self.data_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in nodes_list:
                node_file.write(node['code'])
        write_pipeline_file(self.data_pipeline_dir, nodes_list)

    class Nodes:
        def node_join_datasets(dataset_names: list):
            output_dataset = dataset_wrapper(
                name='joined_dataset',
                type='csv',
                filepath='data/02_intermediate/joined_data.csv',
                layer='intermediate')
            code = """import pandas as pd
from functools import reduce


def join_datasets(*datasets) -> pd.DataFrame:
    return [reduce(lambda left, right: pd.merge(left, right), datasets)]
"""
            return {
                'func': 'join_datasets',
                'name': 'Join_datasets',
                'code': code,
                'inputs': dataset_names,
                'outputs': [output_dataset['name']]
            }, output_dataset
