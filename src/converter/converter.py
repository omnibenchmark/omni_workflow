import os


class ConverterTrait:

    def __init__(self, benchmark_file):
        self.stage_order_map = None
        self.benchmark_file = os.path.abspath(benchmark_file)

    def get_stage_id(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_module_id(self, module):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_definition(self):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_definition_file(self):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_stages(self):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_stage(self, stage_id):
        raise NotImplementedError("Method not implemented yet")

    def get_modules_by_stage(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_implicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_inputs_stage(self, implicit_inputs):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_explicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_outputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_module_excludes(self, module):
        raise NotImplementedError("Method not implemented yet")

    def get_module_parameters(self, module):
        raise NotImplementedError("Method not implemented yet")

    def get_module_repository(self, module):
        raise NotImplementedError("Method not implemented yet")

    def is_initial(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def is_terminal(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_after(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_ids(self):
        raise NotImplementedError("Method not implemented yet")

    def get_module_ids(self):
        raise NotImplementedError("Method not implemented yet")

    def get_output_ids(self):
        raise NotImplementedError("Method not implemented yet")

    def get_initial_datasets(self):
        stages = self.get_benchmark_stages()
        for stage_id in stages:
            stage = stages[stage_id]
            if self.is_initial(stage):
                return self.get_modules_by_stage(stage)

    def get_initial_stage(self):
        stages = self.get_benchmark_stages()
        for stage_id in stages:
            stage = stages[stage_id]
            if self.is_initial(stage):
                return stage

    def get_benchmark_modules(self):
        modules = {}
        stages = self.get_benchmark_stages()
        for stage_id in stages:
            stage = stages[stage_id]
            modules_in_stage = self.get_modules_by_stage(stage)
            modules.update(modules_in_stage)

        return modules

    def stage_order(self, element):
        if self.stage_order_map is None:
            self.stage_order_map = self._compute_stage_order()

        return self.stage_order_map.get(element)

    def _compute_stage_order(self):
        stages = list(self.get_benchmark_stages().values())
        stage_order_map = {self.get_stage_id(stage): pos for pos, stage in enumerate(stages)}
        # FIXME very rudimentary computation of ordering
        # FIXME Might be more complex in future benchmarking scenarios
        # Assuming the order in which stages appear in the benchmark YAML is the actual order of the stages during execution

        return stage_order_map
