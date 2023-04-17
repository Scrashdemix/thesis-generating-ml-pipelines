from pathlib import Path


def generate_data_pipeline(directory: Path):
    with open(directory.joinpath('pipeline.py'), 'w') as file:
        file.write("""from kedro.pipeline import Pipeline, node, pipeline

# from .nodes import ...


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([])
""")
