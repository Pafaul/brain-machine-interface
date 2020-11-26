import http.client
import json
import time
import serial

serial_speed      = 9600
length_of_parsing = 5
parsing_states    = 4
forward_state     = '1'
turn_left_state   = '2'
stop_state        = '3'
working_length    = 15*60

def connect_serial(COM_port):
    port = serial.Serial(COM_port, serial_speed)
    print("Connected to device!")
    time.sleep(5)
    return port

def get_state():
    connection = http.client.HTTPConnection('localhost:336')
    connection.request('GET', '/getlaststate')
    response = connection.getresponse()
    info = json.loads(response.read())
    return [info['state'], info['t']]

def loop_get_state():
    print('Getting states...')

    states = {str(x): y for x, y in zip(range(parsing_states), [0]*parsing_states)}
    states_read = 0

    info = get_state()
    states[info[0]] += 1; timestamp = info[1]

    while states_read < length_of_parsing:
        info = get_state()
        if info[1] == timestamp:
            time.sleep(0.5)
        else:
            states[info[0]] += 1
            timestamp = info[1]
            states_read += 1
        if states[stop_state] != 0:
            break

    return states

def parse_states(states, port):

    if states[stop_state] > 0:
        stop(port)
    elif states[forward_state] > states[turn_left_state]:
        forward(port)
    elif states[turn_left_state] > states[forward_state]:
        turn_left(port)
    elif states[turn_left_state] == states[forward_state]:
        stop(port)

def send_command(port, command):
    port.write(bytes(command, 'UTF-8'))

    
def forward(port):
    print('Going forward...')
    send_command(port, forward_state)
    time.sleep(1.5)
    stop(port)

def turn_left(port):
    print('Turning left...')
    send_command(port, turn_left_state)
    time.sleep(0.4) #0.35 - 90 GRADUSES
    stop(port)

def stop(port):
    print('Stop.')
    send_command(port, stop_state)


def main():
    serial_port_num = input('Input COM-port to connect to: ')
    serial_port = connect_serial(serial_port_num)
    start_time = time.time()
    while time.time() - start_time < working_length:
        states = loop_get_state()
        parse_states(states, serial_port)
        # time.sleep(1.5)
    stop(serial_port)
    serial_port.close()

if __name__ == '__main__':
    main()
