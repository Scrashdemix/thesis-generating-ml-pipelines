from pathlib import Path


def add_hooks(root_dir: Path):
    hooks_file = root_dir.joinpath('src', root_dir.name, 'hooks.py')
    hooks = []
    open(hooks_file, 'w')
    hooks.append(add_hook_data_visualizer(hooks_file, root_dir))
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


def add_hook_data_visualizer(hooks_file:Path, root_dir:Path):
    report_path = Path('../../data/08_reporting/report.html')
    with open(hooks_file, 'a') as file:
        file.write('''from kedro.framework.hooks import hook_impl
import pandas as pd
from pathlib import Path


class DataCatalogVisualizer:

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data: pd.DataFrame) -> None:
        if not isinstance(data, pd.DataFrame): return
        import sweetviz as sv
        report = sv.analyze(data)
        report_path = Path('data/08_reporting/').joinpath(f'{dataset_name}_viz.html')
        report.show_html(filepath=str(report_path), open_browser=False)

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
