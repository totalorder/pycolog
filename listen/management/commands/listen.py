from __future__ import absolute_import

import socket
from django.core.management.base import BaseCommand
import listen.net

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if not listen.net.connection_initiator.isAlive():
            listen.net.connection_initiator.daemon = True
            listen.net.connection_initiator.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8001))
        server_socket.listen(5)

        while 1:
            print "Listening..."
            client_socket, addr = server_socket.accept()
            print "Connection accepted"
            client_thread = listen.net.Worker(client_socket)
            client_thread.daemon = True
            client_thread.start()
