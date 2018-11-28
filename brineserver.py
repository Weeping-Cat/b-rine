import socket
import commands
from threading import Thread

class Server:

    port = 7700
    welcome_message = "--Welcome!--\n"
    new_client_message = "--[CLIENTNAME] joined--"  #text format engine like Pokemon    probably make these functions
    client_left_message = "--[CLIENTNAME] left--" #text format engine like Pokemon
    client_changed_nick_message = "--[CLIENTNAME] changed their name to [NEWCLIENTNAME]--"
    client_list = []
    last_client_n = 0

    def __init__(self):
        self.get_settings()
        self.prepare_connection()

    def get_settings(self):
        settings_file = open("server_config.txt", 'r')
        for line in settings_file:
            line = line.replace('\n', '')   #check how to do better. binary text?
            attr, value = line.split(':')
            setattr(self, attr, int(value))

    def prepare_connection(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))

    def start_host(self):
        while True:
            self.socket.listen(5)
            client, addr = self.socket.accept()
            client.setblocking(False)
            self.on_new_connection(client, addr)

    def on_new_connection(self, client, addr):
        self.last_client_n += 1
        self.create_new_client(client, addr)

    def create_new_client(self, client, addr):
        new_client = Client(' ', (client, addr))
        self.client_list.append(new_client)

    def listen_for_messages(self):
        while True:
            clist = list(self.client_list) #to prevent size change during iteration
            for client in clist:
                try:
                    message = client.client.recv(1024).decode()
                    print(self.on_message_received(message, client)) #don't forget this 'subject to change' print, it's just so it shows a command was used
                except BlockingIOError:
                    pass
                except (ConnectionResetError, ConnectionAbortedError):  #Does this even work? Seems to, remember to confirm
                    m = self.client_left_message.replace('[CLIENTNAME]', client.name)
                    print(m)
                    self.send_to_all(m)
                    self.client_list.remove(client)

    def on_message_received(self, message, client):
        for cmd in commands.command_list:
            if message.startswith(cmd.fname):
                return self._execute_command(cmd, message, client)
        message = client.name+': '+message
        self.send_to_all(message)
        return message

    def _execute_command(self, cmd, message, client):
        args = message.split(' ')
        args.remove(args[0])
        if len(args) == 1:
            args = args[0]   
        return client.name +' used ' + cmd.fname + cmd.execute(client, args, self)  #Need client and server always? try global access like kivy.app

    def send_to_all(self, message):
        for c in self.client_list:
            c.send(message)


class Client:
    def __init__(self, name, connection_tuple):
        self.name = name
        self.client, self.addr = connection_tuple

    def send(self, message):
        try:
            self.client.send(message.encode())
        except (ConnectionResetError, ConnectionAbortedError):
            pass

    
def main():
    server = Server()
    host_thread = Thread(target = server.start_host)
    listen_thread = Thread(target = server.listen_for_messages)
    host_thread.start()
    listen_thread.start()

if __name__ == "__main__":
    main()
        

