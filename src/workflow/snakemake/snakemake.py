import os
from typing import TextIO, List

from src.model import Benchmark, BenchmarkNode
from src.workflow.workflow import WorkflowEngine
from src.workflow.snakemake import rules
from snakemake.cli import main as snakemake_cli

from datetime import datetime

# Module includes for each Snakefile
INCLUDES = [
    "utils.smk",
    "rule_start_benchmark.smk",
    "rule_node.smk",
    "rule_all.smk",
]


class SnakemakeEngine(WorkflowEngine):
    """Snakemake implementation of the WorkflowEngine interface."""

    def run_workflow(self, benchmark: Benchmark, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(),
                     **snakemake_kwargs):
        """
        Serializes & runs benchmark workflow using snakemake.

        Args:
            benchmark (Benchmark): benchmark to run
            cores (int): number of cores to run
            dryrun (bool): validate the snakemake workflow with the benchmark without actual execution
            work_dir (str): working directory
            **snakemake_kwargs: keyword arguments to pass to the snakemake engine

        Returns:
        - Status code of the workflow run.
        """

        # Serialize Snakefile for workflow
        snakefile = self.serialize_workflow(benchmark, work_dir)

        # Prepare the argv list
        argv = self._prepare_argv(snakefile, cores, dryrun, work_dir, **snakemake_kwargs)

        # Execute snakemake script
        success = snakemake_cli(argv)

        return success

    def serialize_workflow(self, benchmark: Benchmark, output_dir: str = os.getcwd()):
        """
        Serializes a Snakefile for the benchmark.

        Args:
            benchmark (Benchmark): benchmark to serialize
            output_dir (str): output directory for the Snakefile

        Returns:
        - Snakefile path.
        """
        os.makedirs(output_dir, exist_ok=True)

        benchmark_file = benchmark.get_definition_file()

        # Serialize Snakemake file
        snakefile_path = os.path.join(output_dir, 'Snakefile')
        with open(snakefile_path, 'w') as f:
            self._write_snakefile_header(f)
            self._write_includes(f, INCLUDES)

            # Load benchmark from yaml file
            f.write(f'benchmark = load("{benchmark_file}")\n\n')

            # Create capture all rule
            f.write("all_paths = sorted(benchmark.get_output_paths())\n")
            f.write("create_all_rule(all_paths)\n\n")

            # Create node rules
            f.write("nodes = benchmark.get_nodes()\n")
            f.write("for node in nodes:\n")
            f.write("    create_node_rule(node, benchmark)\n\n")

        return snakefile_path

    def run_node_workflow(self, node: BenchmarkNode, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(),
                          **snakemake_kwargs):
        """
        Serializes & runs benchmark node workflow using snakemake.

        Args:
            node (Benchmark): benchmark node to run
            cores (int): number of cores to run
            dryrun (bool): validate the snakemake workflow with the benchmark without actual execution
            work_dir (str): working directory
            **snakemake_kwargs: keyword arguments to pass to the snakemake engine

        Returns:
        - Status code of the workflow run.
        """

        os.makedirs(work_dir, exist_ok=True)

        # Serialize Snakefile for node workflow
        snakefile = self.serialize_node_workflow(node, work_dir)

        # Prepare the argv list
        argv = self._prepare_argv(snakefile, cores, dryrun, work_dir, **snakemake_kwargs)

        # Execute snakemake script
        success = snakemake_cli(argv)

        return success

    def serialize_node_workflow(self, node: BenchmarkNode, output_dir: str = os.getcwd()):
        """
        Serializes a Snakefile for a benchmark node.

        Args:
            node (BenchmarkNode): benchmark node to serialize
            output_dir (str): output directory for the Snakefile

        Returns:
        - Snakefile path.
        """
        os.makedirs(output_dir, exist_ok=True)

        benchmark_file = node.get_definition_file()

        # Serialize Snakemake file
        snakefile_path = os.path.join(output_dir, 'Snakefile')
        with open(snakefile_path, 'w') as f:
            self._write_snakefile_header(f)
            self._write_includes(f, INCLUDES)

            # Load benchmark from yaml file
            f.write(f'node = load_node("{benchmark_file}", "{node.get_id()}")\n\n')

            # Create capture all rule
            f.write("input_paths = node.get_input_paths()\n")
            f.write("output_paths = node.get_output_paths()\n")
            f.write("all_paths = input_paths + output_paths\n\n")
            f.write("create_all_rule(all_paths)\n\n")

            # Create node rules
            f.write("create_node_rule(node)\n\n")

        return snakefile_path

    @staticmethod
    def _write_snakefile_header(f: TextIO):
        """Write header for the generated Snakefile"""

        f.write("#!/usr/bin/env snakemake -s\n")
        f.write("##\n")
        f.write("## Snakefile to orchestrate YAML-defined omnibenchmarks\n")
        f.write("##\n")
        f.write(f"## This Snakefile has been automatically generated on {datetime.now()}\n")
        f.write('\n')

    @staticmethod
    def _write_includes(f: TextIO, includes: List[str]):
        """Write includes directive for the generated Snakefile"""

        includes_path = os.path.dirname(os.path.realpath(rules.__file__))
        for include in includes:
            f.write(f'include: "{os.path.join(includes_path, include)}"\n')

        f.write('\n')

    @staticmethod
    def _prepare_argv(snakefile: str, cores: int, dryrun: bool, work_dir: str, **snakemake_kwargs):
        """Prepare arguments to input to the snakemake cli"""

        argv = [
            '--snakefile', snakefile,
            '--cores', str(cores),
            '--directory', work_dir,
        ]

        if dryrun:
            argv.append('--dryrun')

        for key, value in snakemake_kwargs.items():
            if isinstance(value, bool):
                if value:  # Add flag only if True
                    argv.append(f'--{key}')
            else:
                argv.extend([f'--{key}', str(value)])

        return argv
