from pathlib import Path

from generator.utils import generate_pipeline_file_structure
from generator.gen_data_catalog import update_data_catalog
from generator.data_pipeline import DataPipeline

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
    # Data pipeline
    data_pipeline_dir = generate_pipeline_file_structure(root_dir, 'data_pipeline')
    data_pipe = DataPipeline(config=config, data_pipeline_dir=data_pipeline_dir)
    config['datasets'] = data_pipe.get_config()['datasets']
    # Data catalog
    update_data_catalog(config['datasets'], root_directory=root_dir)
    # Data pipeline
    # Train-test split
    # Model pipeline
