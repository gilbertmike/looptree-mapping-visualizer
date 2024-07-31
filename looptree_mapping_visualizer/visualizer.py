from collections.abc import Iterable, Mapping
from typing import Optional, TextIO


TYPE_TO_SHAPE = {
    'temporal': 'box',
    'spatial': 'box',
    'sequential': 'hexagon',
    'parallel': 'hexagon',
    'pipeline': 'hexagon',
    'storage': 'cylinder',
    'compute': 'oval'
}


class DotFile:
    def __init__(self):
        self.content = ''

    def add_node(
        self,
        name: str,
        attributes: Optional[Mapping] = None
    ):
        if attributes is None:
            attributes = {}
        attributes_str = ','.join(
            f'{key}="{value}"' for key, value in attributes.items()
        )

        self.content += f'{name} [{attributes_str}];\n'

    def add_edge(self, src: str, dst: str):
        self.content += f'{src} -- {dst};\n'

    def write_to_stream(self, stream: TextIO):
        stream.write('graph "" {\n')
        stream.write(self.content)
        stream.write('}')


def visualize_mapping(mapping: Mapping) -> DotFile:
    assert mapping['type'] == 'fused'

    counter = Counter()
    dotfile = DotFile()

    _make_segment(None, mapping['nodes'], counter, dotfile)
    return dotfile


class Counter:
    def __init__(self):
        self.count = 0

    def next(self):
        self.count += 1
        return self.count - 1


def _make_segment(
    src: Optional[str],
    nodes: Iterable,
    counter: Counter,
    dotfile: DotFile
):
    for node in nodes:
        node_name = f'n{counter.next()}'
        dotfile.add_node(
            node_name,
            {
                'label': _make_node_label(node),
                'shape': TYPE_TO_SHAPE[node['type']]
            }
        )
        if src is not None:
            dotfile.add_edge(src, node_name)
        src = node_name

        if node['type'] in ['sequential', 'pipeline', 'parallel']:
            for segment in node['branches']:
                _make_segment(src, segment, counter, dotfile)


def _make_node_label(
    node: Mapping
):
    if node['type'] == 'temporal':
        return f"temporal; rank {node['dimension']}; tile size {node['tile_size']}"
    elif node['type'] == 'spatial':
        return f"spatial; rank {node['dimension']}; tile size {node['tile_size']}"
    elif node['type'] == 'storage':
        dspaces_str = ', '.join(node['dspace'])
        return f"{dspaces_str} in buffer {node['target']}"
    elif node['type'] == 'compute':
        return f"{node['einsum']}"
    else:
        return node['type']

