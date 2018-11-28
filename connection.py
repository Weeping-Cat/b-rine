import socket

class Host:
    def __init__(self, port=7700):
        self.s = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.s.bind((self.host, self.port))

        self.s.listen(5)

        c, addr = self.s.accept()
        print('Got connection from '+addr[0])
        c.send(("Thank you for connecting").encode())

        while True:
            data = c.recv(1024).decode()
            if data != '':
                print(data)
                if data == 'quit':
                    c.shutdown()
                    c.close()
    

class Client:
    def __init__(self, address):
        self.s = socket.socket()
        host, port = address.split(':')
        self.s.connect((host, int(port)))
        print(self.s.recv(1024).decode())
        self.s.close

    def send(self, data):
        self.s.send(data.encode())

print('Host or Join')
select = input()
if ':' not in select:
    try:
        select = int(select)
        host = Host(select)
    except:
        host = Host()
else:
    client = Client(select)
    while True:
        client.send(input())
