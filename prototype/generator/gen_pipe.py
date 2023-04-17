from pathlib import Path
import os

from generator.data_pipe import generate_data_pipeline


def generate_pipeline_files(directory: Path, name: str) -> Path:
    directory_path = directory.joinpath(name)
    os.makedirs(directory_path, exist_ok=True)
    open(directory_path.joinpath('__init__.py'), 'w')
    open(directory_path.joinpath('nodes.py'), 'w')
    open(directory_path.joinpath('pipeline.py'), 'w')
    return directory_path

def generate_pipeline(root_directory: str):
    root_directory_path = Path(root_directory)
    pipeline_folder = root_directory_path.joinpath('src', root_directory_path.name, 'pipelines')
    # data pipeline
    data_pipeline_folder = generate_pipeline_files(pipeline_folder, 'data_pipeline')
    generate_data_pipeline(data_pipeline_folder)
    # Train-test split
    # Model training & Model validation
    model_training_folder = generate_pipeline_files(pipeline_folder, 'model_training')
    # Model deployment
