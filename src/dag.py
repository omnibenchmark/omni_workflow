##
##
## Author btraven00
## Source https://github.com/btraven00/runner-tinker/blob/bbcf3c83d3da200e2a206fbc0123f0d8ab6a1b19/bench.py

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, stage_id, module_id, parameters, param_id, inputs, run_id):
        self.stage_id = stage_id
        self.module_id = module_id
        self.parameters = parameters
        self.param_id = f'param_{param_id}' if parameters else 'default'
        self.inputs = inputs
        self.run_id = f'run_{run_id}' if inputs and run_id is not None else 'run'

    def __str__(self):
        return f"Node({self.stage_id}, {self.module_id}, {self.param_id}, {self.run_id})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.stage_id, self.module_id, self.parameters, self.inputs) == \
                   (other.stage_id, other.module_id, other.parameters, other.inputs)
        return False

    def __hash__(self):
        return hash((self.stage_id, self.module_id, self.param_id, self.run_id))


def expend_stage_nodes(converter, stage_id, stage):
    nodes = []

    inputs_for_stage = converter.get_stage_implicit_inputs(stage)
    if not inputs_for_stage or len(inputs_for_stage) == 0:
        inputs_for_stage = [None]

    modules_in_stage = converter.get_modules_by_stage(stage)
    for module_id in modules_in_stage:
        module = modules_in_stage[module_id]
        parameters = converter.get_module_parameters(module)
        if not parameters or len(parameters) == 0:
            parameters = [None]

        # parameters = [None]
        for param_id, param in enumerate(parameters):
            for run_id, input in enumerate(inputs_for_stage):
                run_id = None if len(inputs_for_stage) <= 1 else run_id
                node = Node(stage_id, module_id, param, param_id, input, run_id)
                nodes.append(node)

    return nodes


def build_dag_from_definition(converter):
    g = nx.DiGraph()
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        nodes = expend_stage_nodes(converter, stage_id, stage)
        g.add_nodes_from(nodes)

    for stage_id in stages:
        stage = stages[stage_id]
        after_stage_ids = converter.get_after(stage)
        if after_stage_ids and len(after_stage_ids) > 0:
            for departure_stage_id in after_stage_ids:
                departure_stage = stages[departure_stage_id]
                departure_stage_nodes = expend_stage_nodes(converter, departure_stage_id, departure_stage)
                current_stage_nodes = expend_stage_nodes(converter, stage_id, stage)

                for departure_stage_node in departure_stage_nodes:
                    for current_stage_node in current_stage_nodes:
                        g.add_edge(departure_stage_node, current_stage_node)

    return g


def find_initial_and_terminal_nodes(graph):
    initial_nodes = [node for node, in_degree in graph.in_degree() if in_degree == 0]
    terminal_nodes = [node for node, out_degree in graph.out_degree() if out_degree == 0]
    return initial_nodes, terminal_nodes


def list_all_paths(graph, source, target):
    all_paths = list(nx.all_simple_paths(graph, source=source, target=target))
    return all_paths


def contains_all(path, modules):
    path_modules = [node.module_id for node in path]
    return all(module in path_modules for module in modules)


def exclude_paths(paths, path_exclusions):
    updated_paths = []
    for path in paths:
        should_exclude = False
        for module, excluded_modules in path_exclusions.items():
            for excluded_module in excluded_modules:
                if contains_all(path, [module, excluded_module]):
                    should_exclude = True

        if should_exclude:
            updated_paths.append(path)

    return updated_paths


def get_path_exclusions(converter):
    path_exclusions = {}
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]

        modules_in_stage = converter.get_modules_by_stage(stage)
        for module_id in modules_in_stage:
            module_excludes = converter.get_module_excludes(module_id)
            if module_excludes:
                path_exclusions[module_id] = module_excludes

    return path_exclusions


def construct_output_paths(converter, prefix, nodes):
    if nodes is None or len(nodes) == 0:
        return []
    else:
        head = nodes[0]
        tail = nodes[1:]
        stage_outputs = converter.get_stage_outputs(head.stage_id).values()

        current_path = f'{head.stage_id}/{head.module_id}'
        if any(['{params}' in o for o in stage_outputs]):
            current_path += f'/{head.param_id}'

        if any(['{run}' in o for o in stage_outputs]):
            current_path += f'/{head.run_id}'

        new_prefix = f'{prefix}/{current_path}'
        paths = [x.format(input_dirname=prefix,
                          stage=head.stage_id,
                          module=head.module_id,
                          params=head.param_id,
                          run=head.run_id,
                          name='{name}') for x in stage_outputs]

        return paths + construct_output_paths(converter, new_prefix, tail)


def plot_graph(g, output_file, scale_factor=1.0, node_spacing=0.1, figure_size=(12, 12)):
    layout = nx.circular_layout(g, scale=scale_factor)

    plt.figure(figsize=figure_size)

    nx.draw_networkx_edges(g, layout, edge_color='#AAAAAA')
    nx.draw_networkx_nodes(g, layout, nodelist=g.nodes(), node_size=100, node_color='#fc8d62')
    nodes = [node for node in g.nodes]
    for l in layout:
        layout[l][1] -= node_spacing

    nx.draw_networkx_labels(g, layout, labels=dict(zip(nodes, nodes)), font_size=10)

    # Save the figure to an image file
    plt.savefig(output_file)
