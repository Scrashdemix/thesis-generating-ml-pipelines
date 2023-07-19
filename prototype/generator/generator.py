from pathlib import Path

from generator.utils import generate_pipeline_file_structure
from generator.gen_data_catalog import update_data_catalog
from generator.data_pipeline import DataPipeline
from generator.model_pipeline import ModelPipeline
from generator.hook_writer import add_hooks


def enrich_config(config: dict) -> dict:
    # Add dict for additional information
    config['additional'] = {}
    # Add last datasets name of data pipeline
    config['additional']['data_model_dataset'] = ''
    # Add information about features
    if config.get('features', False):
        config['additional']['features_list'] = list(
                {item: {}} if isinstance(item, str) else item
                for item in config['features']
        )
    else:
        config['additional']['features_list'] = list()
    config['additional']['feature_all_names'] = list({
        k: v
        for d in config['additional']['features_list']
        for k, v in d.items()
        }.keys())
    config['additional']['features_cut_outliers'] = {
        k: v
        for d in config['additional']['features_list']
        for k, v in d.items()
        if v.get('cut_outliers', False)
        }
    config['additional']['scaled_feature_names'] = list({
        k: v
        for d in config['additional']['features_list']
        for k, v in d.items()
        if v.get('scaled', False)
        }.keys())
    return config


def generate(config: dict, root_dir_path: str) -> None:
    root_dir = Path(root_dir_path)
    pipeline_dir = root_dir.joinpath('src', root_dir.name.replace('-', '_'), 'pipelines')
    config = enrich_config(config)
    # Add layer 'raw' to initial datasets
    for ds in config['datasets']:
        if not ds.get('layer', None):
            ds['layer'] = 'raw'
    # Hooks
    add_hooks(root_dir, config)
    # Data pipeline
    data_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'data_pipeline')
    data_pipe = DataPipeline(config, data_pipeline_dir)
    config['datasets'] = data_pipe.get_config()['datasets']

    # Model pipeline
    model_pipeline_dir = generate_pipeline_file_structure(pipeline_dir, 'model_pipeline')
    model_pipe = ModelPipeline(config, root_dir, model_pipeline_dir, first_dataset=data_pipe.get_last_dataset())
    config['datasets'].extend(model_pipe.get_next_datasets())

    # Data catalog
    update_data_catalog(config['datasets'], root_directory=root_dir)
