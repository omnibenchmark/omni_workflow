import os.path


class BenchmarkNode:
    def __init__(self, converter,
                 stage, module, parameters,
                 inputs, outputs,
                 param_id, after=None):

        self.converter = converter
        self.stage = stage
        self.module = module
        self.parameters = parameters
        self.inputs = inputs
        self.outputs = outputs
        self.after = after

        self.stage_id = converter.get_stage_id(stage)
        self.module_id = converter.get_module_id(module)
        self.param_id = f'param_{param_id}' if parameters else 'default'

    def get_id(self):
        return BenchmarkNode.to_id(self.stage_id, self.module_id, self.param_id, self.after)

    def get_definition(self):
        return self.converter.get_benchmark_definition()

    def get_definition_file(self):
        return self.converter.benchmark_file

    def get_inputs(self):
        return self.inputs if self.inputs else []

    def get_input_paths(self):
        input_paths = []
        for input in self.get_inputs():
            input = os.path.basename(input).format(name='input')
            input_paths.append(os.path.join('in', input))

        return input_paths

    def get_outputs(self):
        return self.outputs if self.outputs else []

    def get_output_paths(self):
        output_paths = []
        for output in self.get_outputs():
            output = os.path.basename(output).format(name='output')
            output_paths.append(os.path.join('out', output))

        return output_paths

    def get_parameters(self):
        return self.parameters

    def is_initial(self):
        return self.converter.is_initial(self.stage)

    def get_stage(self):
        return self.stage

    def __str__(self):
        return f"BenchmarkNode({self.get_id()})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BenchmarkNode):
            return (self.stage_id, self.module_id, self.parameters, self.inputs) == \
                (other.stage_id, other.module_id, other.parameters, other.inputs)
        return False

    def __hash__(self):
        return hash(self.get_id())

    @staticmethod
    def to_id(stage_id, module_id, param_id, after_stage_id=None):
        node_id = f'{stage_id}-{module_id}-{param_id}'
        node_id += f'-after_{after_stage_id}' if after_stage_id else ''

        return node_id
