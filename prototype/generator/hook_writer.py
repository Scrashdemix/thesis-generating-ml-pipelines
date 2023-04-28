from pathlib import Path


def add_hooks(root_dir: Path):
    hooks_file = root_dir.joinpath('src', root_dir.name, 'hooks.py')
    hooks = []
    open(hooks_file, 'w')
    hooks.append(add_hook_data_visualizer(hooks_file))
    hooks.append(add_hook_mlflow_tracking(hooks_file))
    add_hooks_to_settings(root_dir, hooks)

def add_hooks_to_settings(root_dir:Path, hook_classes: list):
    classes_string = ', '.join(hook_classes)
    hook_init_string = ''
    for hook in hook_classes:
        hook_init_string  += f'{hook}(),'
    with open(root_dir.joinpath('src', root_dir.name, 'settings.py'), 'w') as file:
        file.write(f'''from {root_dir.name}.hooks import {classes_string}
HOOKS = ({hook_init_string})''')


def add_hook_data_visualizer(hooks_file:Path):
    with open(hooks_file, 'a') as file:
        file.write('''from kedro.framework.hooks import hook_impl
import logging, os
import pandas as pd
import tensorflow as tf


class DataCatalogVisualizer:

    def __init__(self) -> None:
        self.tensorboard_dir = 'summary/'
        os.makedirs(self.tensorboard_dir, exist_ok=True)

    @property
    def _logger(self):
        return logging.getLogger(__name__)

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data: pd.DataFrame) -> None:
        if isinstance(data, pd.DataFrame):
            gen_info_writer = tf.summary.create_file_writer(self.tensorboard_dir)  # .histogram(name="Diabetes Age", data=df['age'])
            with gen_info_writer.as_default():
                try:
                    for feature in data.columns:
                        if data[feature].dtype == 'int64':
                            tf.summary.histogram(name=feature, data=data[feature], step=5)
                            gen_info_writer.flush()
                except:
                    self._logger.warning(f'Dataset {dataset_name} can not be visualized. Type of data: {type(data)}')

''')
    return 'DataCatalogVisualizer'

def add_hook_mlflow_tracking(hooks_file:Path):
    with open(hooks_file, 'a') as file:
        file.write('''import mlflow
from kedro.pipeline.node import Node
class MlFlowTracking:

    @hook_impl
    def after_node_run(self, node:Node):
        if node.name == 'Model_Training':
            mlflow.log_artifact('data/06_models/Model.pickle')
        ''')
    return 'MlFlowTracking'
