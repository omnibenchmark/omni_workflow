from src.converter.converter import ConverterTrait
from src.utils.helpers import merge_dict_list, load_yaml


class LinkMLConverter(ConverterTrait):
    def __init__(self, benchmark_file):
        super().__init__(benchmark_file)
        self.benchmark = load_yaml(benchmark_file)

    def get_benchmark_definition(self):
        return self.benchmark

    def get_stage_id(self, stage):
        return stage.id

    def get_module_id(self, module):
        return module.id

    def get_benchmark_stages(self):
        return dict([(x.id, x) for x in self.benchmark.steps])

    def get_benchmark_stage(self, stage_id):
        stages = self.get_benchmark_stages().values()
        return next(stage for stage in stages if stage.id == stage_id)

    def get_modules_by_stage(self, stage):
        return dict([(x.id, x) for x in stage.members])

    def get_stage_implicit_inputs(self, stage):
        if isinstance(stage, str):
            stage = self.get_benchmark_stages()[stage]

        if stage.initial:
            return []

        return [input.entries for input in stage.inputs]

    def get_inputs_stage(self, implicit_inputs):
        stages_map = {key: None for key in implicit_inputs}
        if implicit_inputs is not None:
            all_stages = self.get_benchmark_stages()
            all_stages_outputs = []
            for stage_id in all_stages:
                outputs = self.get_stage_outputs(stage=stage_id)
                outputs = {key: stage_id for key, value in outputs.items()}
                all_stages_outputs.append(outputs)

            all_stages_outputs = merge_dict_list(all_stages_outputs)
            for in_deliverable in implicit_inputs:
                # beware stage needs to be substituted
                curr_output = all_stages_outputs[in_deliverable]

                stages_map[in_deliverable] = curr_output

        return stages_map

    def get_stage_explicit_inputs(self, implicit_inputs):
        explicit = {key: None for key in implicit_inputs}
        if implicit_inputs is not None:
            all_stages = self.get_benchmark_stages()
            all_stages_outputs = []
            for stage_id in all_stages:
                outputs = self.get_stage_outputs(stage=stage_id)
                outputs = {
                    key: value.format(
                        input_dirname='{input_dirname}',
                        stage=stage_id,
                        module='{module}',
                        params='{params}',
                        name='{name}') for key, value in outputs.items()
                }
                all_stages_outputs.append(outputs)

            all_stages_outputs = merge_dict_list(all_stages_outputs)
            for in_deliverable in implicit_inputs:
                # beware stage needs to be substituted
                curr_output = all_stages_outputs[in_deliverable]

                explicit[in_deliverable] = curr_output

        return explicit

    def get_stage_outputs(self, stage):
        if isinstance(stage, str):
            stage = self.get_benchmark_stages()[stage]

        return dict([(output.id, output.path) for output in stage.outputs])

    def get_module_excludes(self, module):
        if isinstance(module, str):
            module = self.get_benchmark_modules()[module]

        return module.exclude

    def get_module_parameters(self, module):
        params = None
        if module.parameters is not None:
            params = [x.values for x in module.parameters]

        return params

    def get_module_repository(self, module):
        return module.repo

    def is_initial(self, stage):
        if stage.initial:
            return stage.initial
        else:
            return False

    def is_terminal(self, stage):
        if stage.terminal:
            return stage.terminal
        else:
            return False

    def get_after(self, stage):
        return stage.after

    def get_stage_ids(self):
        return [x.id for x in self.benchmark.steps]

    def get_module_ids(self):
        module_ids = []
        for stage in self.benchmark.steps:
            for module in stage.members:
                module_ids.append(module.id)

        return module_ids

    def get_output_ids(self):
        output_ids = []
        for stage in self.benchmark.steps:
            for output in stage.outputs:
                output_ids.append(output.id)

        return output_ids
