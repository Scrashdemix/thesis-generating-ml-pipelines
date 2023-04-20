from pathlib import Path
import os


def generate_pipeline_file_structure(root_dir: Path, name: str) -> Path:
    pipeline_dir = root_dir.joinpath('src', root_dir.name, 'pipelines')
    new_pipeline_dir = pipeline_dir.joinpath(name)
    os.makedirs(new_pipeline_dir, exist_ok=True)
    with open(new_pipeline_dir.joinpath('__init__.py'), 'w') as file:
        file.write('from .pipeline import create_pipeline')
    open(new_pipeline_dir.joinpath('nodes.py'), 'w')
    open(new_pipeline_dir.joinpath('pipeline.py'), 'w')
    return new_pipeline_dir

def generate_nodes_list(nodes_config: dict) -> tuple:
    names = []
    nodes_code = ''
    for name, info in nodes_config:
        pass

def write_pipeline_file(pipeline_dir: Path, nodes_list: list) -> None:
    func_str = ', '.join([n['func'] for n in nodes_list])
    nodes_code = ''
    with open(pipeline_dir.joinpath('pipeline.py'), 'w') as file:
        for node in nodes_list:
            nodes_code += f'''
            node(
                func={node['func']},
                inputs={str(node['inputs'])},
                outputs={str(node['outputs'])},
                name='{node['name']}',
            ),'''
            file.write(f"""from kedro.pipeline import Pipeline, node, pipeline

from .nodes import {func_str}


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [{nodes_code}
        ]
    )
""")
