install:
	pipx install pipenv
	pipenv install -r requirements.txt
activate:
	pipenv shell
serialize:
	python main.py --benchmark_file=$(if $(benchmark_file),$(benchmark_file),'data/Benchmark_001.yaml')
benchmark:
	snakemake -p --cores 1
dry:
	snakemake -p --cores 1 -n -p -F
graph:
	snakemake --dag | dot -Tpng > workflow_dag.png
clean:
	rm -f benchmark.pkl Snakefile
	rm -rf ./in ./out ./log ./data/D1 ./data/D2 workflow_dag.png output_dag.png
