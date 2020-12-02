from math import floor,ceil

def maximum(sequence, stop_state):
    element_dict = {str(e): 0 for e in sequence}
    for element in sequence:
        element_dict[str(element)] += 1

    max_state = -1
    max_state_count = -1
    for element in element_dict.keys():
        if element_dict[str(element)] > max_state_count:
            max_state = element
            max_state_count = element_dict[str(element)]

    return [max_state]

def maximum_sequential(sequence, stop_state):
    longest_state = -1
    longest_chain_length = -1
    current_state = -1
    current_state_length = -1

    for state in sequence:
        if state == current_state:
            current_state_length += 1
        else:
            if (current_state_length > longest_chain_length):
                longest_chain_length = current_state_length
                longest_state = current_state

    return [longest_state]

def mean_state(sequence, stop_state, rounding_function):
    state_mean = 0
    for state in sequence:
        state_mean += state

    state_mean = rounding_function(state_mean/len(sequence))
    return [state_mean]

def mean_state_floor(sequence, stop_state):
    return mean_state(sequence, stop_state, floor)

def mean_state_ceil(sequence, stop_state):
    return mean_state(sequence, stop_state, ceil)