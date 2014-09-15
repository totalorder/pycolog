from threading import Thread
from Queue import Queue
from listen.models import Logger, Entry
import re

sentinel = object()

class Worker(Thread):
    def __init__(self, client_socket):
        super(Worker, self).__init__()
        self.client_socket = client_socket

    def run(self):
        line = ""
        header = ""
        while 1:
            data = self.client_socket.recv(64)
            if not data:
                print "No header recevied. Connection closed"
                header = None
                break
            header += data
            newline = header.find("\n")
            if newline != -1:
                line = header[newline:]
                header = header[:newline].strip()
                break

        if not header:
            self.client_socket.send("No header received. Closing connection...")
            self.client_socket.close()
            return
        print "Received header %s" % header
        logger, created = Logger.objects.get_or_create(name=header)
        if created:
            print "Created new logger with name: %s" % logger.name
        regex = re.compile(logger.regex, re.IGNORECASE)
        while 1:
            data = self.client_socket.recv(1024)
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
                            entry = Entry(logger=logger, data=entry_data)
                            entry.save()
                            print "Saved entry %s: \"%s\"" % (entry.id, entry.data)
                        line = line[start:]
                        offset = 0
                    else:
                        break
            else:
                print "Connection closed"
                break

class ConnectionInitiator(Thread):
    def __init__(self):
        super(ConnectionInitiator, self).__init__()
        self.queue = Queue()

    def run(self):
        while 1:
            print "Waiting for connection..."
            client_socket = self.queue.get()
            print "Connection established"
            client_thread = Thread(client_socket)
            client_thread.daemon = True
            client_thread.start()


connection_initiator = ConnectionInitiator()