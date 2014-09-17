from copy import copy
import json
import socket
from threading import Thread
from Queue import Queue
import time
from listen.models import Logger, Entry
import re
import traceback


class Worker(Thread):
    def __init__(self, client_socket, addLoggerCallback, removeLoggerCallback):
        super(Worker, self).__init__()
        self.addLoggerCallback = addLoggerCallback
        self.removeLoggerCallback = removeLoggerCallback
        self.client_socket = client_socket

    def run(self):
        logger = None
        try:
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
            self.addLoggerCallback(logger.id)
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
                    self.removeLoggerCallback(logger.id)
                    break
        except Exception:
            traceback.print_exc()
            self.removeLoggerCallback(logger.id)

class ConnectionInitiator(Thread):
    def __init__(self, addLoggerCallback, removeLoggerCallback):
        super(ConnectionInitiator, self).__init__()
        self.addLoggerCallback = addLoggerCallback
        self.removeLoggerCallback = removeLoggerCallback
        self.queue = Queue()

    def connect(self, address):
        self.queue.put(address)

    def run(self):
        while 1:
            print "Waiting for new connection request..."
            address = self.queue.get()
            print "Connecting to %s!" % address
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect(address)
            except Exception as e:
                print "Failed to connect to %s: %s" % (address, e)
                continue

            client_thread = Worker(client_socket, self.addLoggerCallback, self.removeLoggerCallback)
            client_thread.daemon = True
            client_thread.start()


class ConnectionListener(Thread):
    def __init__(self, addLoggerCallback, removeLoggerCallback):
        super(ConnectionListener, self).__init__()
        self.addLoggerCallback = addLoggerCallback
        self.removeLoggerCallback = removeLoggerCallback
        self.queue = Queue()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8001))
        server_socket.listen(5)

        while 1:
            print "Listening for incoming connections..."
            client_socket, addr = server_socket.accept()
            print "Incoming connection accepted!"
            client_thread = Worker(client_socket, self.addLoggerCallback, self.addLoggerCallback)
            client_thread.daemon = True
            client_thread.start()

class BackgroundServer:
    def __init__(self):
        self._running_loggers = set()

    def addLogger(self, logger):
        self._running_loggers.add(logger)

    def removeLogger(self, logger):
        self._running_loggers.remove(logger)

    def getRunningLoggers(self):
        return tuple(self._running_loggers)

    def run(self):
        self.connection_initiator = ConnectionInitiator(self.addLogger, self.removeLogger)
        self.connection_initiator.daemon = True
        self.connection_initiator.start()

        self.connection_listener = ConnectionListener(self.addLogger, self.removeLogger)
        self.connection_listener.daemon = True
        self.connection_listener.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8002))
        server_socket.listen(5)

        print "Listening for status requests..."
        while 1:
            client_socket, addr = server_socket.accept()
            print "Accepted status request!"
            data = ""
            try:
                while 1:
                    new_data = client_socket.recv(1024)
                    if new_data:
                        data += new_data
                        if len(data) >= 4:
                            if data[:4] == "STAT":
                                client_socket.send(json.dumps(self.getRunningLoggers()))
                                client_socket.close()
                                break
                            elif data[:4] == "CONN" and len(data) == 26:
                                new_address = data[5:].strip().split(":")
                                self.connection_initiator.connect(new_address)
                                client_socket.close()
                                break
                    else:
                        break
            except Exception as e:
                print "Failed to connect process request: %s" % e
                print data

class ListenClient:
    def __init__(self, interval=5):
        self.interval = interval
        self.last_fetch = time.time() - self.interval
        self.cached_status_info = []

    def getStatusInformation(self):
        if time.time() - self.interval > self.last_fetch:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("127.0.0.1", 8002))
            client_socket.send("STAT")
            data = ""
            while 1:
                new_data = client_socket.recv(1024)
                if new_data:
                    data += new_data
                else:
                    break
            self.cached_status_info = json.loads(data)
            self.last_fetch = time.time()
        return self.cached_status_info

    def connectLogger(self, address):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8002))
        client_socket.send("CONN %s" % address.rjust(21))
        data = ""
        while 1:
            new_data = client_socket.recv(1024)
            if new_data:
                data += new_data
            else:
                break

listen_client = ListenClient()