from src.workflow.workflow import WorkflowEngine
from src.workflow.snakemake import rules
import os
import pickle
from datetime import datetime


class SnakemakeEngine(WorkflowEngine):
    def __init__(self, benchmark):
        super().__init__(benchmark)

    def run_workflow(self):
        raise NotImplementedError("Method not implemented yet")

    def serialize_workflow(self, output_path=os.getcwd()):
        os.makedirs(output_path, exist_ok=True)

        # Dump benchmark pickle file
        benchmark_path = os.path.join(output_path, "benchmark.pkl")
        with open(benchmark_path, "wb") as f:
            pickle.dump(self.benchmark, f)

        # Define includes
        includes = [
            "utils.smk",
            "rule_start_benchmark.smk",
            "rule_node.smk",
            "rule_all.smk"
        ]

        # Serialize Snakemake file
        snakefile_path = os.path.join(output_path, 'Snakefile')
        with open(snakefile_path, 'w') as f:
            self._write_snakefile_header(f)
            self._write_includes(f, includes)

            # Load benchmark from pickle file
            f.write(f'benchmark = load_benchmark("{benchmark_path}")\n\n')

            # Create capture all rule
            f.write("all_paths = sorted(benchmark.get_output_paths())\n")
            f.write("create_all_rule(all_paths)\n\n")

            # Create node rules
            f.write("nodes = benchmark.get_nodes()\n")
            f.write("for node in nodes:\n")
            f.write("    create_node_rule(benchmark, node)\n\n")

        return snakefile_path

    def run_node_workflow(self, node):
        raise NotImplementedError("Method not implemented yet")

    def serialize_node_workflow(self, node, output_path=os.getcwd()):
        raise NotImplementedError("Method not implemented yet")

    def _write_snakefile_header(self, f):
        f.write("#!/usr/bin/env snakemake -s\n")
        f.write("##\n")
        f.write("## Snakefile to orchestrate YAML-defined omnibenchmarks\n")
        f.write("##\n")
        f.write(f"## This Snakefile has been automatically generated on {datetime.now()}\n")
        f.write('\n')

    def _write_includes(self, f, includes):
        includes_path = os.path.dirname(os.path.realpath(rules.__file__))
        for include in includes:
            f.write(f'include: "{os.path.join(includes_path, include)}"\n')

        f.write('\n')