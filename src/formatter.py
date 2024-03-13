
## f-strings: rule maker
## wildcards: output mapper (only params, currently)
# def format_dataset_templates_to_be_expanded(dataset):
#     filled = []
#     for stage in self.config['steps'].keys():
#         if 'initial' in self.config['steps'][stage].keys() and self.config['steps'][stage]['initial']:
#              outs = list(get_stage_outputs(stage).values())
#              for i in range(len(outs)):
#                  filled.append([outs[i].format(stage = stage, mod = dataset, params = '{params}', id = dataset)])

#     return(sum(filled, []))
def format_dataset_templates_to_be_expanded(converter, dataset):
    filled = []
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        if converter.is_initial(stage):
            outs = list(converter.get_stage_outputs(stage).values())
            for i in range(len(outs)):
                filled.append([outs[i].format(stage=stage_id, module='{dataset}', params='{params}', name='{dataset}')])

    return sum(filled, [])


## f-strings: rule maker
## wildcards (single curly bracket): expanded from the output mapper
def format_output_templates_to_be_expanded(converter, stage_id, module_id):
    o = [x.format(input_dirname='{pre}',
                  stage=stage_id,
                  module=module_id,
                  params='{params}',
                  name='{id}') for x in converter.get_stage_outputs(stage_id).values()]

    return o


def format_input_templates_to_be_expanded(converter, stage_id, module_id):
    return 'todo'