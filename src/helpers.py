import yaml
import re
import omni_schema.datamodel.omni_schema as model
from linkml_runtime.loaders import yaml_loader


def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        try:
            yaml_data = yaml.safe_load(file)
            return yaml_data
        except yaml.YAMLError as e:
            print(f"Error loading YAML file '{file_path}': {e}")
            return None


def load_benchmark(file_path):
    benchmark = yaml_loader.load(file_path, model.Benchmark)
    return benchmark


def merge_dict_list(list_of_dicts):
    merged_dict = {key: value for d in list_of_dicts if d is not None for key, value in d.items()}

    return merged_dict


def make_folder_name_safe(parameter_value):
    # Replace unsafe characters with safe alternatives
    safe_value = parameter_value.replace(" ", "_").replace(".", "_")

    return safe_value


def format_name(path, prefix):
    pattern = fr'{prefix}/.+?/([^/]+)/.+?$'
    name = re.match(pattern, path)[1]
    new_path = path.format(name=name)

    return new_path


