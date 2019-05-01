import asyncio

from collections import defaultdict


class ClientServerProtocol(asyncio.Protocol):
    DICT_DATA = defaultdict(set)

    def run_server(self, host, port): #TODO
        return host, port

    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, data):
        status, _ = data.split(" ", 1)
        if status in 'put':
            _, payload = data.split(" ", 1)
            payload = payload.strip()
            for row in payload.split("\n"):
                key, value, timestamp = row.split()
                ClientServerProtocol.DICT_DATA[key].add((value, timestamp))
            return f'ok\n\n'
        elif status in 'get *':
            string = ''
            for key, value in ClientServerProtocol.DICT_DATA.items():
                for val, timestamp in value:
                    string += f'{key} {val} {timestamp}\n'
            return 'ok\n'+string + '\n'
        else:
            return 'error\nwrong command\n'


    def data_received(self, data):
        resp = self.process_data(data.decode())
        print(resp)
        self.transport.write(resp.encode())


test = ClientServerProtocol()
test.run_server('127.0.0.1', 8181)

loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8182
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
