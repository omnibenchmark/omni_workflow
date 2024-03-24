import re

## f-strings: rule maker
## wildcards (single curly bracket): expanded from the output mapper
def format_output_templates_to_be_expanded(converter, stage_id, initial=False):
    input_dirname = 'out' if initial else '{pre}'
    stage_outputs = converter.get_stage_outputs(stage_id).values()
    o = [x.replace('{input_dirname}', input_dirname) for x in stage_outputs]

    if not initial:
        o = [re.sub(r'\/.*\/', '/{post}/', x, count=1) for x in o]

    # print(f'Output: {stage_id}: {o}')
    return o


def extract_stages_from_path(path, known_stages):
    parts = path.split('/')
    stages = []

    i = 1
    while i < len(parts) - 1:
        if parts[i] in known_stages:
            j = i+1

            while j < len(parts) and parts[j] not in known_stages:
                j += 1

            sub_parts = parts[i:j]

            assert 2 <= len(sub_parts) <= 4
            stages.append(tuple(sub_parts))
            i = j
        else:
            i += 1

    return stages


def match_node_format(to_match):
    if type(to_match) is str:
        to_match = to_match.split('/')

    stage_id = to_match[0]
    module_id = to_match[1]
    if len(to_match) == 2:
        param_id, run_id = 'default', 'run'
    elif len(to_match) == 3:
        param_id = to_match[2] if 'param_' in to_match[2] else 'default'
        run_id = to_match[2] if 'run_' in to_match[2] else 'run'
    else:
        param_id = to_match[2]
        run_id = to_match[3]

    return stage_id, module_id, param_id, run_id


def match_input_module(input, stages, name):
    expected_input_module = input.split('{input_dirname}/')[1].split('/{module}')[0]
    matching_stage = next((tup for tup in stages if tup[0] == expected_input_module), None)

    if matching_stage:
        matched_module = matching_stage[1]

        input = input.replace('{input_dirname}', '{pre}')
        input = input.replace('{module}', matched_module)
        input = input.replace('{name}', name)
        if '{params}' in input:
            matched_params = next((x for x in matching_stage[2:] if 'param' or 'default' in x), None)
            input = input.replace('{params}', matched_params)

        if '{run}' in input:
            matched_run = next((x for x in matching_stage[2:] if 'run' in x), None)
            input = input.replace('{run}', matched_run)

        return input
    else:
        print(f'Could not find matching stage for {input} in {stages}')
        return None


def match_input_prefix(input, pre):
    stage = f'/{input.split("/")[1]}'
    matched_prefix = pre.split(stage)[0]
    formatted_input = input.format(pre=matched_prefix)

    # print(f'Input: {input} Prefix: {pre} Formatted: {formatted_input}')
    return formatted_input


def match_inputs(inputs, stages, pre, name):
    all_matched = True

    formatted_inputs = []
    for input in inputs:
        formatted_input = match_input_module(input, stages, name)
        if not formatted_input:
            all_matched = False
            break
        else:
            formatted_input = match_input_prefix(formatted_input, pre)
            formatted_inputs.append(formatted_input)

    return formatted_inputs if all_matched else []


def format_input_templates_to_be_expanded(converter, nodes, output_paths, wildcards):
    pre = wildcards.pre
    post = wildcards.post
    name = wildcards.name

    pre_stages = extract_stages_from_path(pre, converter.get_benchmark_stages())

    stage_id, module_id, param_id, run_id = match_node_format(post)
    node_hash = hash((stage_id, module_id, param_id, run_id))
    matching_node = next((node for node in nodes if hash(node) == node_hash), None)
    assert matching_node is not None

    node_implicit_inputs = matching_node.inputs
    node_inputs = converter.get_stage_explicit_inputs(node_implicit_inputs).values()

    inputs = match_inputs(node_inputs, pre_stages, pre, name)
    for i in inputs:
        assert i in output_paths

    # print(f'Inputs: {stage_id} {module_id} {param_id} {run_id}: {inputs}')
    return inputs
