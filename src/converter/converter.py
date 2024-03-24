

class SnakemakeConverterTrait:
    def get_benchmark_definition(self):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_stages(self):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_stage(self, stage_id):
        raise NotImplementedError("Method not implemented yet")

    def get_modules_by_stage(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_benchmark_modules(self):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_implicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_explicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_outputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_module_excludes(self, module):
        raise NotImplementedError("Method not implemented yet")

    def get_module_parameters(self, module):
        raise NotImplementedError("Method not implemented yet")

    def is_initial(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def is_terminal(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_after(self, stage):
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
