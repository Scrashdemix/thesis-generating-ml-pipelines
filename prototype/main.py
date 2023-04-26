import yaml
from argparse import ArgumentParser

from generator.generator import generate


def parse_arguments() -> str:
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        help="YAML file for configuration",
        metavar="FILE"
    )
    parser.add_argument(
        "-l",
        "--location",
        dest="location",
        help="Root directory of the kedro project whose pipeline should be generated",
        metavar="Directory"
    )
    args = parser.parse_args()
    return {'filename': args.filename, 'location': args.location}

def read_yaml_file(file_arg: str) -> dict:
    if file_arg:
        with open(file_arg, 'r') as file:
            content = yaml.safe_load(file)
    else:
        with open(input("Please provide a valid configuration file:"), 'r') as file:
            content = yaml.safe_load(file)
    return content

if __name__ == "__main__":
    args = parse_arguments()
    config = read_yaml_file(args['filename'])
    generate(config, root_dir_path=args['location'])
