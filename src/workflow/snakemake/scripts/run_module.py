#! /usr/bin/env python
##
## A benchmarking (fake) step parsing params, inputs and outputs
##
## Started 22 Feb 2024
## Izaskun Mallona

import sys
import os
from typing import List

from snakemake.script import Snakemake


def mock_execution(inputs: List[str], output: str, snakemake: Snakemake):
    print('Processed', inputs, 'to', output, 'using threads', snakemake.threads)
    print('  bench_iteration is', snakemake.bench_iteration)
    print('  resources are', snakemake.resources)
    print('  wildcards are', snakemake.wildcards)
    print('  rule is', snakemake.rule)
    print('  scriptdir is', snakemake.scriptdir)
    print('  params are', snakemake.params)


def dump_parameters_to_file(output_dir: str, parameters: str):
    if parameters is not None:
        params_file = os.path.join(output_dir, 'parameters.txt')
        with open(params_file, 'w') as params_file:
            params_file.write(f'{parameters}')

        param_dict_file = os.path.join(output_dir, '..', 'parameters_dict.txt')
        with open(param_dict_file, 'a') as param_dict_file:
            param_dict_file.write(f'{os.path.basename(output_dir)} {parameters}\n')


try:
    snakemake: Snakemake = snakemake
    parameters = dict(snakemake.params)['parameters']
    output_dir = os.path.dirname(snakemake.output[0])
    os.makedirs(output_dir, exist_ok=True)

    dump_parameters_to_file(output_dir, parameters)

    for out in snakemake.output:
        with open(out, 'w') as sys.stdout:
            mock_execution(inputs=snakemake.input,
                           output=out,
                           snakemake=snakemake)

except NameError:
    raise RuntimeError("This script must be run from within a Snakemake workflow.")




