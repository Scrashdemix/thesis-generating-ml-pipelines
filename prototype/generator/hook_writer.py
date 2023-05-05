from pathlib import Path
from typing import Dict, List, Set, Tuple


def add_hooks(root_dir: Path, config: Dict):
    hooks_file = root_dir.joinpath('src', root_dir.name, 'hooks.py')
    imports = set()
    classes = []
    hooks = []
    if not config.get('visualization', None) is None:
        imp, cls, hook_name = add_hook_data_visualizer()
        imports.update(imp)
        classes.append(cls)
        hooks.append(hook_name)
    imp, cls, hook_name = add_hook_mlflow_tracking()
    imports.update(imp)
    classes.append(cls)
    hooks.append(hook_name)
    write_hooks_file(hooks_file, imports, classes)
    add_hooks_to_settings(root_dir, hooks)


def write_hooks_file(hooks_file: Path, imports: Set, classes: List):
    with open(hooks_file, 'w') as file:
        file.write('\n'.join(imports))
        for cls in classes:
            file.write('\n\n\n' + cls)


def add_hooks_to_settings(root_dir:Path, hook_classes: List):
    classes_string = ', '.join(hook_classes)
    hook_init_string = ''
    for hook in hook_classes:
        hook_init_string  += f'{hook}(),'
    with open(root_dir.joinpath('src', root_dir.name, 'settings.py'), 'w') as file:
        file.write(f'''from {root_dir.name}.hooks import {classes_string}

HOOKS = ({hook_init_string})
''')


def add_hook_data_visualizer() -> Tuple[List, str, str]:
    """Returns import, code and class name of the data visualizer hook."""
    imports = ['from kedro.framework.hooks import hook_impl',
               'import pandas as pd',
               'from pathlib import Path']
    code = '''class DataCatalogVisualizer:

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data: pd.DataFrame) -> None:
        if not isinstance(data, pd.DataFrame): return
        import sweetviz as sv
        report = sv.analyze(data)
        report_path = Path('data/08_reporting/').joinpath(f'{dataset_name}_viz.html')
        report.show_html(filepath=str(report_path), open_browser=False)'''
    return imports, code, 'DataCatalogVisualizer'


def add_hook_mlflow_tracking() -> Tuple[List, str, str]:
    imports = ['import mlflow',
               'import pandas as pd',
               'from kedro.pipeline.node import Node',
               'from kedro.framework.hooks import hook_impl']
    code = '''class MlFlowTracking:

    @hook_impl
    def after_node_run(self, node:Node):
        if node.name == 'Model_Training':
            mlflow.log_artifact('data/06_models/Model.pickle')'''
    return imports, code, 'MlFlowTracking'
