from pathlib import Path

from generator.utils import generate_pipeline_file_structure
from generator.gen_data_catalog import update_data_catalog
from generator.data_pipeline import DataPipeline
from generator.feature_pipeline import FeatureEngineering
from generator.training_pipeline import TrainingPipeline
from generator.hook_writer import add_hooks

# structure:
#   data pipeline
#       Data Ingestion: conf/base/catalog.yml
#       Data Visualization
#       Data preprocessing steps: placeholder
#       Train-test split
#       Data normalization steps: placeholder
#   model pipeline
#   deployment pipeline

def generate(config: dict, root_dir_path: str) -> None:
    root_dir = Path(root_dir_path)
    pipeline_dir = root_dir.joinpath('src', root_dir.name, 'pipelines')
    config['nodes'] = []
    # Hooks
    add_hooks(root_dir)
    # Data pipeline
    data_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'data_pipeline')
    data_pipe = DataPipeline(config, data_pipeline_dir)
    config['datasets'] = data_pipe.get_config()['datasets']
    # Feature engineering pipeline
    feature_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'feature_pipeline')
    feature_pipe = FeatureEngineering(config, root_dir, feature_pipeline_dir, last_datasets=data_pipe.get_next_datasets())
    # Training pipeline
    training_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'training_pipeline')
    training_pipe = TrainingPipeline(config, root_dir, training_pipeline_dir, last_datasets=feature_pipe.get_next_datasets())
    config['datasets'].append(training_pipe.get_next_datasets()[0])
    # Data catalog
    update_data_catalog(config['datasets'], root_directory=root_dir)
    # Data pipeline
    # Train-test split
    # Model pipeline
