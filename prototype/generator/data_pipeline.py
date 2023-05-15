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
        self.nodes_list = []
        self.last_dataset = ''  # names of datasets for next pipelines
        self._structure()
        self._write_files()

    def get_config(self):
        return self.config
    
    def get_additional_datasets(self):
        return self.additional_datasets
    
    def get_last_dataset(self):
        return self.last_dataset
    
    def _structure(self):
        node_jd, dataset_jd = self.Nodes.node_join_datasets(dataset_names=[ds['name'] for ds in self.config['datasets']])
        self.nodes_list.append(node_jd)
        self.config['datasets'].append(dataset_jd)
        self.last_dataset = dataset_jd['name']
        if len(self.config['additional']['features_cut_outliers']) > 0:
            node_co, dataset_co = self.Nodes.node_remove_outliers(self.config)
            self.nodes_list.append(node_co)
            self.config['datasets'].append(dataset_co)
            self.last_dataset = dataset_co['name']
    
    def _write_files(self):
        with open(self.data_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in self.nodes_list:
                node_file.write(node['code'])
        write_pipeline_file(self.data_pipeline_dir, self.nodes_list)

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

        def node_remove_outliers(config: dict):
            conditions = []
            for cond in config['additional']['features_cut_outliers']:
                conditions.append(f'''(df['{cond}'] < df['{cond}'].quantile(0.95))''')
                conditions.append(f'''(df['{cond}'] > df['{cond}'].quantile(0.05))''')
            cond_str = ' & '.join(conditions)
            code = f'''
def cut_outliers(df: pd.DataFrame) -> pd.DataFrame:
    return [df[{cond_str}]]
'''
            output_dataset = dataset_wrapper(name='prm_dataset', type='memory', layer='primary')
            return {
                'func': 'cut_outliers',
                'name': 'Cut_outliers',
                'code': code,
                'inputs': ['joined_dataset'],
                'outputs': [output_dataset['name']]
            }, output_dataset
