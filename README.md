# omnibenchmark workflow

Powered by Snakemake

# How to

- `make install` to install dependencies
- `make activate` to activate the environment with the dependencies (pipenv shell)
- `make benchmark` to run the benchmark (= trigger the Snakefile)
- `make dry` to dry run the benchmark (= dry run the Snakefile)
- `make clean` deletes the `./out` and `./log` output folders

# Rationale

Parse a YAML specification of a benchmark and dynamically build snakemake rules to build the suitable workflow.

# Branches

Develop in branch `dev`, seldom merged to `main`

# Started

05 Feb 2024, Izaskun Mallona
