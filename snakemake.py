from src.converter import BenchmarkConverter
from src.helpers import *
import src.dag as dag
import src.formatter as fmt


benchmark = load_benchmark('data/Benchmark_001.yaml')
converter = BenchmarkConverter(benchmark)
G = dag.build_dag_from_definition(converter)
path_exclusions = dag.get_path_exclusions(converter)
initial_nodes, terminal_nodes = dag.find_initial_and_terminal_nodes(G)

all_paths = set()
prefix = 'out'
for initial_node in initial_nodes:
    for terminal_node in terminal_nodes:
        paths = dag.list_all_paths(G, initial_node, terminal_node)
        paths_after_exclusion = dag.exclude_paths(paths, path_exclusions)

        for path in paths_after_exclusion:
            paths = dag.construct_output_paths(converter, prefix=prefix, nodes=path)
            all_paths.update(paths)


all_paths = [format_name(path, prefix) for path in list(all_paths)]


def format_output_templates_to_be_expanded(stage_id, initial=False):
    return fmt.format_output_templates_to_be_expanded(converter, stage_id, initial)


def format_input_templates_to_be_expanded(wildcards):
    return fmt.format_input_templates_to_be_expanded(converter, G.nodes, all_paths, wildcards)
