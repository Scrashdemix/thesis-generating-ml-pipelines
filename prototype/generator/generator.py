
from generator.gen_data import update_data_catalog
from generator.gen_pipe import generate_pipeline

# structure:
#   data pipeline
#       Data Ingestion: conf/base/catalog.yml
#       Data Visualization
#       Data preprocessing steps: placeholder
#       Train-test split
#       Data normalization steps: placeholder
#   model pipeline
#   deployment pipeline

def generate(config: dict, location: str) -> None:
    update_data_catalog(config['Datasets'], root_directory=location)
    generate_pipeline(root_directory=location)
