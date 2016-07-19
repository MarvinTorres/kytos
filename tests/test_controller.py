import time
from socket import socket
from socketserver import BaseRequestHandler
from threading import Thread
from unittest import TestCase

from pyof.v0x01.symmetric.vendor_header import VendorHeader

from kyco.controller import Controller
from kyco.core.buffers import KycoEventBuffer
from kyco.core.events import KycoRawEvent
from kyco.core.tcp_server import KycoOpenFlowRequestHandler
from kyco.core.tcp_server import KycoServer


HOST = '127.0.0.1'
PORT = 6633


class TestKycoController(TestCase):

    def setUp(self):
        self.controller = Controller()
        self.thread = Thread(name='Controller',
                             target=self.controller.start)
        self.thread.start()
        time.sleep(1)
        print("sleeping")
        time.sleep(1)

    def test_one_connection(self):
        message = VendorHeader(xid=1, vendor=5)
        client = socket()
        client.connect((HOST, PORT))
        client.send(message.pack())
        client.close()

    def tearDown(self):
        self.controller.stop()
        self.thread.join()
        while self.thread.is_alive():
            pass