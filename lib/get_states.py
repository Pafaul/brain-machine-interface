import http.client
import json

from numpy import random


class GetState:
    @staticmethod
    def get_state_server(server_url: str) -> list:
        connection = http.client.HTTPConnection(server_url)
        try:
            while True:
                connection.request('GET', '/getlaststate')
                response = connection.getresponse()
                info = json.loads(response.read())
                yield [info['state'], info['t']]
        except Exception:
            connection.close()
            print('Error during server request')
            yield None

    @staticmethod
    def get_state_from_file(filename: str, separator: str = ',') -> list:
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            time, state = line.strip().split(separator)
            yield [state, time]
        yield None

    @staticmethod
    def get_state_random_uniform(lower_bound: int, upper_bound: int, length_of_sequence: int = 1000) -> list:
        for time in range(length_of_sequence):
            yield [int(random.randint(lower_bound, high=upper_bound+1)), time]
        yield None

