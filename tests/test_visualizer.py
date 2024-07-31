from pathlib import Path
import unittest

from ruamel.yaml import YAML
yaml = YAML(typ='safe')

from looptree_mapping_visualizer.visualizer import visualize_mapping


class TestVisualizer(unittest.TestCase):
    def test_visualizer(self):
        config = yaml.load(
            Path(__file__).parent / 'configs' / 'looptree-test.yaml'
        )
        dotfile = visualize_mapping(config['mapping'])
        lines = dotfile.content.splitlines()
        edges = [
            'n0 -- n1;',
            'n1 -- n2;',
            'n2 -- n3;',
            'n3 -- n4;',
            'n4 -- n5;',
            'n5 -- n6;',
            'n5 -- n7;'
        ]
        for e in edges:
            self.assertTrue(e in lines)
