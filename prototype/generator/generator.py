from pathlib import Path

from generator.utils import generate_pipeline_file_structure
from generator.gen_data_catalog import update_data_catalog
from generator.data_pipeline import DataPipeline
from generator.feature_pipeline import FeatureEngineering
from generator.model_pipeline import ModelPipeline
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
    pipeline_dir = root_dir.joinpath('src', root_dir.name.replace('-', '_'), 'pipelines')
    config['nodes'] = []
    # Hooks
    add_hooks(root_dir, config)
    # Data pipeline
    data_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'data_pipeline')
    data_pipe = DataPipeline(config, data_pipeline_dir)
    config['datasets'] = data_pipe.get_config()['datasets']

    # Feature engineering pipeline
    #feature_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'feature_pipeline')
    #feature_pipe = FeatureEngineering(config, root_dir, feature_pipeline_dir, last_datasets=data_pipe.get_next_datasets())

    # Model pipeline
    model_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'model_pipeline')
    model_pipe = ModelPipeline(config, root_dir, model_pipeline_dir, last_datasets=data_pipe.get_next_datasets())
    config['datasets'].extend(model_pipe.get_next_datasets())

    # Data catalog
    update_data_catalog(config['datasets'], root_directory=root_dir)
    # Data pipeline
    # Train-test split
    # Model pipeline
