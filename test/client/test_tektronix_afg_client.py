#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for TektronixAFGClient.

This module contains unit tests for the `TektronixAFGClient` class,
using mocking to simulate the RPC server interactions.

__author__ = "Marco Bonaglia"
__version__ = "1.0.0"
__date__ = "2025-06-09"
"""

import unittest
from unittest import mock
from plico_io.tektronix_afg.client.tektronix_afg_client import TektronixAFGClient
from plico_io.utils.timeout import Timeout


class TestTektronixAFGClient(unittest.TestCase):
    """Tests the TektronixAFGClient class."""

    def setUp(self):
        """Set up the test case by mocking the ZmqRemoteProcedureCall."""
        self.mock_request_socket_patcher = mock.patch(
            'plico.rpc.zmq_remote_procedure_call.ZmqRemoteProcedureCall.requestSocket')
        self.mock_request_socket_func = self.mock_request_socket_patcher.start()
        self.mock_request_socket = mock.Mock()
        self.mock_request_socket_func.return_value = self.mock_request_socket

        self.client = TektronixAFGClient(host="localhost", port=7100)
        self.mock_send_request = mock.Mock() # Reset mock_send_request
        self.client._rpc.sendRequest = self.mock_send_request

    def tearDown(self):
        """Clean up after the test case."""
        self.mock_request_socket_patcher.stop()

    def test_turn_on(self):
        """Test turn_on method sends correct RPC request."""
        self.mock_send_request.return_value = True
        result = self.client.turn_on(channel=1)
        self.assertTrue(result)
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'turnOn', 1, timeout=Timeout.SETTER)

    def test_turn_off(self):
        """Test turn_off method sends correct RPC request."""
        self.mock_send_request.return_value = True
        result = self.client.turn_off(channel=2)
        self.assertTrue(result)
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'turnOff', 2, timeout=Timeout.SETTER)

    def test_get_status(self):
        """Test get_status method sends correct RPC request and returns value."""
        self.mock_send_request.return_value = True
        result = self.client.get_status(channel=1)
        self.assertTrue(result)
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'getStatus', 1, timeout=Timeout.GETTER)

    def test_list_devices(self):
        """Test list_devices method sends correct RPC request and returns value."""
        expected_devices = {
            "1": {"name": "Channel 1", "type": "Tektronix AFG Channel"},
            "2": {"name": "Channel 2", "type": "Tektronix AFG Channel"}
        }
        self.mock_send_request.return_value = expected_devices
        devices = self.client.list_devices()
        self.assertEqual(devices, expected_devices)
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'listDevices', timeout=Timeout.GETTER)

    def test_set_function(self):
        """Test set_function method sends correct RPC request."""
        self.client.set_function(channel=1, function="SIN")
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'setFunction', 1, "SIN", timeout=Timeout.SETTER)

    def test_set_frequency(self):
        """Test set_frequency method sends correct RPC request."""
        self.client.set_frequency(channel=1, frequency=1000, unit="Hz")
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'setFrequency', 1, 1000, "Hz", timeout=Timeout.SETTER)

    def test_set_amplitude(self):
        """Test set_amplitude method sends correct RPC request."""
        self.client.set_amplitude(channel=2, amplitude=5.0, unit="Vpp")
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'setAmplitude', 2, 5.0, "Vpp", timeout=Timeout.SETTER)

    def test_set_offset(self):
        """Test set_offset method sends correct RPC request."""
        self.client.set_offset(channel=1, offset=1.0, unit="V")
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'setOffset', 1, 1.0, "V", timeout=Timeout.SETTER)

    def test_print_settings(self):
        """Test print_settings method sends correct RPC request."""
        self.client.print_settings()
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'printSettings', timeout=Timeout.GETTER)

    def test_get_snapshot(self):
        """Test get_snapshot method sends correct RPC request and returns value."""
        expected_snapshot = {"snapshot": "client_test_snapshot"}
        self.mock_send_request.return_value = expected_snapshot
        snapshot = self.client.get_snapshot()
        self.assertEqual(snapshot, expected_snapshot)
        self.mock_send_request.assert_called_once_with(
            self.client._requestSocket, 'getSnapshot', timeout=Timeout.GETTER)

    def test_close(self):
        """Test close method closes sockets."""
        self.client.close()
        self.mock_request_socket.close.assert_called_once()
        # Since _statusSocket is None by default, it shouldn't try to close it


if __name__ == '__main__':
    unittest.main() 