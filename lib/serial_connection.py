import time
import serial

class DummyPort:
    def write(self, *args):
        return True

    def close():
        pass

def connect_serial(COM_port: str, serial_speed: int = 9600):
    try:
        port = serial.Serial(COM_port, serial_speed)
    except Exception:
        return None

    time.sleep(5)
    return port

def dummy_serial(*args, **argv):
    return DummyPort()

def port_wrapper(port: object, payload: int, time_to_sleep: float = 0.5):
    try:
        port.write(bytes(payload, 'UTF-8'))
        time.sleep(time_to_sleep)
    except Exception:
        exception_text = 'Error during sending information to device'
        print(exception_text)
        raise Exception(exception_text)