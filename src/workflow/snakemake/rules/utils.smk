from src.converter import LinkMLConverter
from src.model import Benchmark
from src.validation import Validator


def load(benchmark_file_path):
    converter = LinkMLConverter(benchmark_file_path)
    validator = Validator()
    converter = validator.validate(converter)
    benchmark = Benchmark(converter)

    return benchmark


def load_node(benchmark_file_path, node_id):
    benchmark = load(benchmark_file_path)
    return benchmark.get_node_by_id(node_id)