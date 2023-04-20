import os, yaml
from pathlib import Path

from config import constants


def get_dataset_type(type: str) -> str:
    if not type:
        raise ValueError(f'Dataset type cannot be of {type}')
    try:
        return constants.dataset_type[str.lower(type)]
    except:
        raise KeyError(f'There is no valid kedro dataset type for key {type}')

def build_dataset_dict(dataset: dict) -> dict:
    """
    Builds a dictionary which conforms with kedros catalog.yml from the dataset specification.
    
    Params:
        dataset: dict which contains information about a single dataset
    Returns:
        dict which contains information about a single dataset and conforms with kedros catalog.yml spec
    """
    dataset_type = get_dataset_type(dataset['type'])
    ds = {
        dataset['name']: {
            'type': dataset_type,
            'filepath': dataset['filepath'],
            }
        }
    if (dataset.get('load_args', False)):  # add load_args
        ds[dataset['name']]['load_args'] = dataset['load_args']
    if (dataset.get('save_args', False)):  # add save_args
        ds[dataset['name']]['save_args'] = dataset['save_args']
    if (dataset.get('credentials', False)):  # add credentials
        ds[dataset['name']]['credentials'] = dataset['credentials']

    # HTTP(s) can't be versioned
    if (dataset.get('versioned', False) and str(dataset['filepath']).startswith('http')):
        raise ValueError(f"Dataset {dataset['name']} cannot be versioned because HTTP(s) does not support versioning.")
    else:
        ds[dataset['name']]['versioned'] = dataset.get('versioned', False)

    # Add file_format to spark spec
    if (str.lower(dataset['type']) == 'spark' and 
        dataset.get('file_format', False)):
        ds[dataset['name']]['file_format'] = dataset['file_format']
    return ds

def update_data_catalog(datasets: list, root_directory: Path) -> None:
    catalog_path = root_directory.joinpath(constants.data_catalog_path).absolute()
    # Ensure conf/base/catalog.yaml exists
    if not os.path.exists(catalog_path):
        raise FileNotFoundError("Catalog.yml doesn't exist in the project folder.")
    # write datasets into file
    if len(datasets) == 0:  # return if no datasets were specified
        return
    with open(catalog_path, "w") as catalog_file:
        for dataset in datasets:
            yaml.dump(build_dataset_dict(dataset=dataset), catalog_file, sort_keys=False)