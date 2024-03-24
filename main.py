import src.formatter as fmt
from src.dag import *
from src.helpers import *
from src.converter import BenchmarkConverter


class FakeWildcards:
    def __init__(self):
        self.pre = None
        self.post = None
        self.name = None


if __name__ == "__main__":
    benchmark = load_benchmark('data/Benchmark_001.yaml')
    converter = BenchmarkConverter(benchmark)
    print(converter.get_benchmark_definition())

    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        stage_name = stage['name']
        print('Stage', stage_name)

        modules_in_stage = converter.get_modules_by_stage(stage)
        print('  ', stage_name, 'with modules', modules_in_stage.keys(), '\n')
        print('  Implicit inputs:\n', converter.get_stage_implicit_inputs(stage))
        print('  Explicit inputs:\n', [converter.get_stage_explicit_inputs(i)
                                       for i in converter.get_stage_implicit_inputs(stage)])
        print('  Outputs\n', converter.get_stage_outputs(stage))
        print('------')

        for module_id in modules_in_stage:
            module = modules_in_stage[module_id]
            module_name = module['name']
            print('  Module', module_name)
            print('    Excludes:', converter.get_module_excludes(module))
            print('    Params:', converter.get_module_parameters(module))
        print('------')

    print('------')

    G = build_dag_from_definition(converter)
    path_exclusions = get_path_exclusions(converter)
    plot_graph(G, output_file='output_dag.png', scale_factor=1.5, node_spacing=0.2)
    initial_nodes, terminal_nodes = find_initial_and_terminal_nodes(G)

    all_paths = set()
    for initial_node in initial_nodes:
        for terminal_node in terminal_nodes:
            paths = list_all_paths(G, initial_node, terminal_node)
            paths_after_exclusion = exclude_paths(paths, path_exclusions)

            for path in paths_after_exclusion:
                paths = construct_output_paths(converter, prefix='out', nodes=path)
                all_paths.update(paths)

    all_paths = [format_name(path, 'out') for path in list(all_paths)]

    wildcards = FakeWildcards()
    wildcards.pre = 'out/data/D1/process/P1/param_0/methods/M1/default/run_1'
    wildcards.post = 'metrics/m3'
    wildcards.name = 'D1'
    fmt.format_input_templates_to_be_expanded(converter, G.nodes, all_paths, wildcards)
