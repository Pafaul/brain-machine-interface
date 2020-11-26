def match_with_template(parsed_states_sequence, template, acceptable_state_error):
    errors = []
    if len(parsed_states_sequence) != len(template):
        return None

    for state, template_state, index in zip(parsed_states_sequence, template, list(range(len(template)))):
        if state != template_state:
            errors.append([state, template_state, index])
    
    if (len(errors) <= acceptable_state_error):
        return True
    else:
        return False

def find_template_in_sequence(parsed_states_sequence, template, acceptable_state_error):
    is_in_sequence = False
    template_length = len(template)
    for index in range(len(parsed_states_sequence)-template_length):
        is_in_sequence = match_with_template(parsed_states_sequence[index:index+template_length], template, acceptable_state_error)
        if is_in_sequence:
            return [is_in_sequence, index]

    return [is_in_sequence, -1]