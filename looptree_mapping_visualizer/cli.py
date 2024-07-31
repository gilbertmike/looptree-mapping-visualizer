import argparse
from collections.abc import Iterable
from pathlib import Path
import sys

from ruamel.yaml import YAML
yaml = YAML(typ='safe')

from looptree_mapping_visualizer.visualizer import visualize_mapping


def main():
    parser = argparse.ArgumentParser(
        description='Convert LoopTree mapping YAML to DOT'
    )
    parser.add_argument('files',
                        type=str,
                        nargs='+',
                        help='YAML files to convert')

    args = parser.parse_args(sys.argv[1:])

    for fname in args.files:
        config = yaml.load(Path(fname))
        dotfile = visualize_mapping(config['mapping'])
        dotfile.write_to_stream(sys.stdout)
