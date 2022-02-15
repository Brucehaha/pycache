import socket
from gevent.server import StreamServer

from src.command_parser import parse_command
from src.commands_handler import handle_command, resp_error


def read_from_client(s, address):
    while 1:
        try:
            data = s.recvfrom(66356)
            if data is not None and data[0] is not None:
                try:
                    command_arr = parse_command(data[0].decode('utf-8'), 0)
                    response = handle_command(command_arr)
                    s.send(bytes(response, 'utf-8'))
                except socket.error:
                    raise
                except Exception as e:
                    s.send(bytes(resp_error(f"An unspecified eror occured. {e}"), "utf-8"))
        except socket.error:
            print(socket.error)
            break

    s.close()

def bind_server(ip, port, spawn_limit):
    """
    create service
    :return:
    """
    try:
        server = StreamServer((ip, port), read_from_client, spawn=spawn_limit)  # create new service
        server.serve_forever()
    except Exception as e:
        print(str(e))
        server.close() if server is not None and server.started else None