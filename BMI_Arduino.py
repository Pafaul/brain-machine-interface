import http.client
import json
import time
import serial

serial_speed      = 9600
length_of_parsing = 3
parsing_states    = 4
forward_state     = '1'
turn_left_state   = '2'
stop_state        = '3'
working_length    = 1*60

def connect_serial(COM_port):
    port = serial.Serial(COM_port, serial_speed)
    print("Connected to device!")
    time.sleep(5)
    return port

def get_state():
    connection = http.client.HTTPConnection('localhost:336')
    connection.request('GET', '/getlaststate')
    response = connection.getresponse()
    state = json.loads(response.read())['state']
    return state

def loop_get_state():
    start_time = time.time()
    states = {str(x): y for x, y in zip(range(parsing_states), [0]*parsing_states)}

    while time.time() - start_time < length_of_parsing:
        states[get_state()] += 1
        time.sleep(1)

    return states

def parse_states(states, port):

    if states[stop_state] > 0:
        stop()
        send_command(port, stop_state)
    elif states[forward_state] > states[turn_left_state]:
        forward()
        send_command(port, forward_state)
    elif states[turn_left_state] > states[forward_state]:
        turn_left()
        send_command(port, turn_left_state)
    elif states[turn_left_state] == states[forward_state]:
        stop()
        send_command(port, stop_state)

def send_command(port, command):
    port.write(bytes(command, 'UTF-8'))

    
def forward():
    print('Going forward')

def turn_left():
    print('Turning left')

def stop():
    print('Stop')

def main():
    serial_port_num = input('Input port to connect to:')
    serial_port = connect_serial(serial_port_num)
    start_time = time.time()
    while time.time() - start_time < working_length:
        states = loop_get_state()
        parse_states(states, serial_port)
        time.sleep(2)
        send_command(serial_port, '3')
    serial_port.close()

if __name__ == '__main__':
    main()
