import configparser

from sys import argv

from lib.template_creation import create_templates_from_file
from lib.template_matching import *
from lib.get_states import *
from lib.parsing_functions import *
from lib.serial_connection import *


def setup_server(configuration: list):
    server_type = configuration['server']['server_type']
    if (server_type == 'cortex'):
        return GetState.get_state_server(configuration['server']['server_url'])
    elif (server_type == 'file'):
        return GetState.get_state_from_file(configuration['server']['server_url'])
    elif (server_type == 'random'):
        lower_bound = 0
        upper_bound = int(configuration['parsing']['total_states'])-1
        time = int(configuration['default']['working_time'])
        return GetState.get_state_random_uniform(lower_bound, upper_bound, time)
    else:
        raise Exception(f'Unknown server type: {server_type}')


def setup_serial(configuration: list) -> object:
    serial_type = configuration['serial']['com_port_to_use']
    if (serial_type == 'dummy'):
        return dummy_serial()
    else:
        try:
            serial_speed = int(configuration['serial']['serial_connection_speed'])
            return connect_serial(serial_type, serial_speed)
        except Exception:
            raise Exception(f'Cannot connect to {serial_type} device')


def setup_templates(configuration: list) -> dict:
    template_file = configuration['parsing']['template_file']
    try:
        templates = create_templates_from_file(template_file)
        return templates
    except FileNotFoundError:
        raise Exception(f'File {template_file} not found ')


def setup_parsing_functions(configuration: list):
    function_name = configuration['parsing']['parsing_function']
    if (function_name == 'maximum'):
        return maximum
    elif (function_name == 'maximum_seq'):
        return maximum_sequential
    elif (function_name == 'mean_state_floor'):
        return mean_state_floor
    elif (function_name == 'mean_state_ceil'):
        return mean_state_ceil
    else:
        raise Exception(f'Parsing function {function_name} not found')

 
def setup_consts(configuration: list) -> dict:
    constants = dict(configuration['default'])
    constants['state_sequence_length'] = configuration['parsing']['state_sequence_length']
    constants['max_template_length'] = configuration['parsing']['max_template_length']
    for key in constants.keys():
        if '.' not in constants[key]:
            constants[key] = int(constants[key])
        else:
            constants[key] = float(constants[key])
    return constants


def parse_configuration_file(config_file: str) -> list:
    '''
    Возвращает: константы, функция для обработки состояний, шаблоны, итератор получения информации, serial порт
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    setup = []
    setup_functions = [
        setup_consts,
        setup_parsing_functions,
        setup_templates,
        setup_server,
        setup_serial
    ]

    for function in setup_functions:
        setup.append(function(config))
    
    return setup


def loop(config: list):
    constants, parse_func, templates, server, serial_port = config
    current_states = []
    
    try:
        while True:
            if (len(current_states) < constants['state_sequence_length']):
                local_states = []
                for _ in range(int(constants['max_template_length'])):
                    state, t = next(server)
                    local_states.append(state)
                state = parse_func(local_states, constants['stop_state'])
                current_states.append(state[0])
                continue
            
            if (current_states == [constants['stop_state']]*constants['stop_states_to_exit']):
                raise Exception('EMERGENCY STOP REQUIRED')

            for template_name in templates.keys():
                template = templates[template_name]
                if (match_with_template(current_states, template[0], 0)):
                    print(f'Template: {template_name}')
                    print(template, current_states)
                    serial_port.write(template[1])
                    current_states=current_states[len(template):]
                    break
            else:
                states_sequence = ' '.join(current_states)
                print(f'No template matches sequence {states_sequence}')
                current_states.pop(0)

    except Exception as e:
        print(e)

    finish(config)

  
def finish(config):
    constants, parse_func, templates, server, serial_port = config
    serial_port.close()

def main():
    if (len(argv) != 2):
        raise Exception(f'Invalid arguments lenght.\nOne argument required: path to configuration file.')
    else:
        configuration = parse_configuration_file(argv[1])
        loop(configuration)

if __name__ == "__main__":
    main()