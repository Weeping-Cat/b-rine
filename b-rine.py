from brineserver import Server
from threading import Thread

server = Server()

host_thread = Thread(target = server.start_host)
listen_thread = Thread(target = server.listen_for_messages)

host_thread.start()
listen_thread.start()
