from __future__ import absolute_import
import socket
from django.core.management.base import BaseCommand, CommandError
from listen.models import Entry
import re

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8001))
        server_socket.listen(5)

        regex = re.compile(r"(\[(error|warning|info|debug)])", re.IGNORECASE)
        while 1:
            print "Listening..."
            client_socket, addr = server_socket.accept()
            print "Connection accepted"

            line = ""
            header = ""
            while 1:
                data = client_socket.recv(64)
                if not data:
                    print "No header recevied. Connection closed"
                    header = None
                    break
                header += data
                newline = header.find("\n")
                if newline != -1:
                    line = header[newline:]
                    header = header[:newline]
                    break

            if header is None:
                continue
            print "Received header %s" % header
            while 1:
                data = client_socket.recv(1024)
                if data:
                    line += data
                    offset = 0
                    while 1:
                        match = regex.search(line, offset)
                        if match:
                            start = match.start()
                            if not match.start():
                                offset += 1
                                continue

                            entry_data = line[:start].strip()

                            if entry_data:
                                entry = Entry(logger=header, data=entry_data)
                                entry.save()
                                print "Saved entry %s: \"%s\"" % (entry.id, entry.data)
                            line = line[start:]
                            offset = 0
                        else:
                            break
                else:
                    print "Connection closed"
                    break
