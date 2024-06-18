import os
import os.path as op

from src.utils.helpers import merge_dict_list
from src.converter.converter import ConverterTrait


class YamlConverter(ConverterTrait):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def get_benchmark_definition(self):
        return self.config

    def get_stage_id(self, stage):
        return stage['id']

    def get_module_id(self, module):
        return module['id']

    def get_benchmark_stages(self):
        return dict([(x['id'], x) for x in self.config['steps']])

    def get_benchmark_stage(self, stage_id):
        stages = self.get_benchmark_stages()
        return [stage for stage in stages if stage['id'] == stage_id]

    def get_modules_by_stage(self, stage):
        return dict([(x['id'], x) for x in stage['members']])

    def get_modules(self):
        m = []
        for (stage_name, stage) in self.get_benchmark_stages():
            m.append([x['id'] for x in stage['members']])

        return sum(m, [])

    def get_module_parameters(self, module):
        params = None
        if 'parameters' in module.keys():
            params = [x['values'] for x in module['parameters']]

        return params

    def get_module_repository(self, module):
        return module['repo']

    def get_module_excludes(self, module):
        excludes = None
        if 'exclude' in module.keys():
            excludes = module['exclude']

        return excludes

    def get_stage_implicit_inputs(self, stage):
        if isinstance(stage, str):
            stage = self.get_benchmark_stages()[stage]

        if 'initial' in stage.keys() and stage['initial']:
            return None

        return [input['entries'] for input in stage['inputs']]

    def get_stage_outputs(self, stage):
        if isinstance(stage, str):
            stage = self.get_benchmark_stages()[stage]

        return dict([(output['id'], output['path']) for output in stage['outputs']])

    def get_stage_explicit_inputs(self, implicit_inputs):
        explicit = {key: None for key in implicit_inputs}
        if implicit_inputs is not None:
            all_stages = self.get_benchmark_stages()
            all_stages_outputs = [self.get_stage_outputs(stage=stage_id) for stage_id in all_stages]
            all_stages_outputs = merge_dict_list(all_stages_outputs)

            for in_deliverable in implicit_inputs:
                 # beware stage needs to be substituted
                curr_output = all_stages_outputs[in_deliverable]

                explicit[in_deliverable] = curr_output

        return explicit

    def get_stage_explicit_input_dirnames(self, stage):
        explicit = self.get_stage_explicit_inputs(stage)
        de = explicit
        if explicit is not None:
            for i in range(len(explicit)):
                for in_deliverable in explicit[i].keys():
                    de[i][in_deliverable] = op.dirname(explicit[i][in_deliverable])

        return de

    def is_initial(self, stage):
        if 'initial' in stage.keys() and stage['initial']:
            return True
        else:
            return False

    def is_terminal(self, stage):
        if 'terminal' in stage.keys() and stage['terminal']:
            return True
        else:
            return False

    def get_after(self, stage):
        if 'after' in stage.keys():
            return stage['after']
        else:
            return None

    def get_initial_dataset_paths(self, dataset):
        filled = []
        for stage in self.config['steps'].keys():
            if 'initial' in self.config['steps'][stage].keys() and self.config['steps'][stage]['initial']:
                outs = list(self.get_stage_outputs(stage).values())
                for i in range(len(outs)):
                    filled.append([outs[i].format(stage=stage, mod=dataset, params='default', id=dataset)])

        return sum(filled, [])

    ## playground -------------

    # # dirty, fix
    # def write_module_flag_for_dirty_module_wildcards(module):
    #     stage = get_initial_stage_name()
    #     ## creates an empty file
    #     open(op.join('out', stage,  f"{module}/{module}.flag".format(module = module)), 'a')

    def tokenize_parameters(self):
        print('todo')

    def count_path_depth(self, path):
        return path.count(os.sep)

    ## if a module (stage) gets inputs from different modules, i.e. counts from 'processed' after 'raw'
    ##   and 'meta' from raw, then we have to nest outputs after the longest (deepest) folder -
    ##   that is, raw/processed/here, and not to raw/here
    def get_deepest_input_dirname(self, stage):
        ii = self.get_stage_implicit_inputs(stage)
        deepest_inputs = []
        if ii is not None:
            deepest_input = '.'
            deepest_input_depth = 0
            for input_dict in ii:
                for item in input_dict.keys():
                    curr_depth = self.count_path_depth(input_dict[item])
                    if curr_depth > deepest_input_depth:
                        deepest_input_depth = curr_depth
                        deepest_input = op.dirname(input_dict[item])
                        deepest_inputs.append(deepest_input)

        return deepest_inputs

    def get_deepest_input_dirname_for_input_dict(self, input_dict_list):
        deepest_input = '.'
        deepest_input_depth = 0
        for input_dict in input_dict_list:
            for item in input_dict.keys():
                curr_depth = self.count_path_depth(input_dict[item])
                if curr_depth > deepest_input_depth:
                    deepest_input_depth = curr_depth
                    deepest_input = op.dirname(input_dict[item])

        return deepest_input

    # ## with substituted module/stage/ids
    # def fill_explicit_outputs(stage, module):
    #     i = get_stage_explicit_outputs(stage)
    #     idir = get_deepest_input_dirname(stage)

    #     oe = get_stage_outputs(stage)
    #     excludes = get_module_excludes(stage = stage, module = module)
    #     return('todo')

    def nest_deliverable_path(self, parent, path):
        return op.join(parent, path)

    ## using the input identifiers, excludes and parameters and not 'after' clauses
    def traverse_yaml(self):
        lookup = ''
        for (stage_name, stage) in self.get_benchmark_stages():
            for module in self.get_modules_by_stage(stage):
                ii = self.get_stage_implicit_inputs(stage)

        return 'todo'
