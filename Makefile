install:
	pipx install pipenv
	pipenv install -r requirements.txt
activate:
	pipenv shell
test:
	python main.py --benchmark_file=$(benchmark_file)
benchmark:
	snakemake -p --cores 1
dry:
	snakemake -p --cores 1 -n -p -F
graph:
	snakemake --dag | dot -Tpng > workflow_dag.png
clean:
	rm -rf ./out ./log ./data/D1 ./data/D2 workflow_dag.png output_dag.png
