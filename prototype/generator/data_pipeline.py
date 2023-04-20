from pathlib import Path
from generator.utils import write_pipeline_file


class DataPipeline:

    def __init__(self, config: dict, data_pipeline_dir: Path) -> None:
        '''
        Params:
        pipeline_dir: path to directory called 'data_pipeline'
        '''
        if ('nodes' in config.keys()):
            raise RuntimeError(
                "There should not be any nodes configuration in the pipelines config at time of initialization."
            )
        self.config = config
        self.data_pipeline_dir = data_pipeline_dir
        self._structure()
        self._write_files()

    def get_config(self):
        return self.config
    
    def _structure(self):
        nodes_list = []
        nodes_list.append(
            self.Nodes.node_join_datasets(
                dataset_names=[ds['name'] for ds in self.config['datasets']],
                output_name='joined_dataset'
            ))
        self.config['nodes'] = nodes_list
        self.config['datasets'].append({
            'name': 'joined_dataset',
            'type': 'csv',
            'filepath': 'data/02_intermediate/joined_data.csv',
        })
    
    def _write_files(self):
        nodes_list = self.config['nodes']
        with open(self.data_pipeline_dir.joinpath('nodes.py'), 'w') as node_file:
            for node in nodes_list:
                node_file.write(node['code'])
        write_pipeline_file(self.data_pipeline_dir, nodes_list)

    class Nodes:
        def node_join_datasets(dataset_names: list, output_name: str):
            code = """import pandas as pd
from functools import reduce


def join_datasets(*datasets) -> pd.DataFrame:
    return reduce(lambda left, right: pd.merge(left, right), datasets)
"""
            return {
                'func': 'join_datasets',
                'name': 'Join_datasets',
                'code': code,
                'inputs': dataset_names,
                'outputs': [output_name]
            }
