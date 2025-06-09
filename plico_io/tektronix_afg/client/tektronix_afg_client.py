#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tektronix AFG Client

This module provides a client for the Tektronix AFG waveform generator server,
allowing remote control and monitoring of the instrument via RPC.

__author__ = "Marco Bonaglia"
__version__ = "1.0.0"
__date__ = "2025-06-09"
"""

import time
import json
from plico.utils.logger import Logger
from plico.rpc.zmq_ports import ZmqPorts
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico_io.client.abstract_controller_client import AbstractControllerClient
from plico_io.utils.timeout import Timeout


class TektronixAFGClient(AbstractControllerClient):
    """Client class for interacting with the Tektronix AFG server.

    This class provides methods to control the Tektronix AFG waveform generator
    through the PLICO server.
    """

    def __init__(self, host: str, port: int, name: str = None):
        """Create a Tektronix AFG client instance.

        Args:
            host: Hostname or IP address of the Tektronix AFG server.
            port: Port number of the Tektronix AFG server.
            name: Name of the client instance, by default None.
        """
        self._name = name or f"TektronixAFGClient-{host}:{port}"
        self._host = host
        self._port = port
        self._logger = Logger.of(self._name)

        # Initialize RPC
        self._rpc = ZmqRemoteProcedureCall()

        # Initialize sockets
        self._requestSocket = self._rpc.requestSocket(self._host, self._port)
        self._statusSocket = None  # Status socket is optional

        self._logger.notice(f"Tektronix AFG client initialized for {host}:{port}")

    def turn_on(self, channel: int, timeout_in_sec: float = Timeout.SETTER):
        """Turn on a specified channel of the Tektronix AFG.

        Args:
            channel: The channel number to turn on (1 or 2).
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.

        Returns:
            True if successful, False otherwise.
        """
        self._logger.notice(f"Turning on channel {channel}")
        return self._rpc.sendRequest(self._requestSocket, 'turnOn', channel, timeout=timeout_in_sec)

    def turn_off(self, channel: int, timeout_in_sec: float = Timeout.SETTER):
        """Turn off a specified channel of the Tektronix AFG.

        Args:
            channel: The channel number to turn off (1 or 2).
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.

        Returns:
            True if successful, False otherwise.
        """
        self._logger.notice(f"Turning off channel {channel}")
        return self._rpc.sendRequest(self._requestSocket, 'turnOff', channel, timeout=timeout_in_sec)

    def get_status(self, channel: int, timeout_in_sec: float = Timeout.GETTER):
        """Get the current output status of a specified channel.

        Args:
            channel: The channel number to check (1 or 2).
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.GETTER`.

        Returns:
            True if the channel is on, False if it's off.
        """
        self._logger.debug(f"Getting status for channel {channel}")
        return self._rpc.sendRequest(self._requestSocket, 'getStatus', channel, timeout=timeout_in_sec)

    def list_devices(self, timeout_in_sec: float = Timeout.GETTER):
        """List all available devices (channels) on the Tektronix AFG.

        Args:
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.GETTER`.

        Returns:
            A dictionary of devices.
        """
        self._logger.debug("Listing devices")
        return self._rpc.sendRequest(self._requestSocket, 'listDevices', timeout=timeout_in_sec)

    def set_function(self, channel: int, function: str, timeout_in_sec: float = Timeout.SETTER):
        """Sets the waveform function for the specified channel.

        Args:
            channel: The channel number (1 or 2).
            function: The waveform function to set.
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.
        """
        self._logger.notice(f"Setting function for channel {channel} to {function}")
        self._rpc.sendRequest(self._requestSocket, 'setFunction', channel, function, timeout=timeout_in_sec)

    def set_frequency(self, channel: int, frequency: float, unit: str = "Hz", timeout_in_sec: float = Timeout.SETTER):
        """Sets the frequency for the specified channel.

        Args:
            channel: The channel number (1 or 2).
            frequency: The frequency value.
            unit: The unit of frequency. Defaults to "Hz".
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.
        """
        self._logger.notice(f"Setting frequency for channel {channel} to {frequency}{unit}")
        self._rpc.sendRequest(self._requestSocket, 'setFrequency', channel, frequency, unit, timeout=timeout_in_sec)

    def set_amplitude(self, channel: int, amplitude: float, unit: str = "Vpp", timeout_in_sec: float = Timeout.SETTER):
        """Sets the amplitude for the specified channel.

        Args:
            channel: The channel number (1 or 2).
            amplitude: The amplitude value.
            unit: The unit of amplitude. Defaults to "Vpp".
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.
        """
        self._logger.notice(f"Setting amplitude for channel {channel} to {amplitude}{unit}")
        self._rpc.sendRequest(self._requestSocket, 'setAmplitude', channel, amplitude, unit, timeout=timeout_in_sec)

    def set_offset(self, channel: int, offset: float, unit: str = "V", timeout_in_sec: float = Timeout.SETTER):
        """Sets the DC offset for the specified channel.

        Args:
            channel: The channel number (1 or 2).
            offset: The offset value.
            unit: The unit of offset. Defaults to "V".
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.SETTER`.
        """
        self._logger.notice(f"Setting offset for channel {channel} to {offset}{unit}")
        self._rpc.sendRequest(self._requestSocket, 'setOffset', channel, offset, unit, timeout=timeout_in_sec)

    def print_settings(self, timeout_in_sec: float = Timeout.GETTER):
        """Prints the current settings of both channels on the server-side console.

        Args:
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.GETTER`.
        """
        self._logger.debug("Requesting server to print settings")
        self._rpc.sendRequest(self._requestSocket, 'printSettings', timeout=timeout_in_sec)

    def get_snapshot(self, timeout_in_sec: float = Timeout.GETTER):
        """Get a snapshot of the Tektronix AFG server state.

        Args:
            timeout_in_sec: Timeout in seconds. Defaults to `Timeout.GETTER`.

        Returns:
            Snapshot information.
        """
        self._logger.debug("Getting snapshot")
        return self._rpc.sendRequest(self._requestSocket, 'getSnapshot', timeout=timeout_in_sec)

    def close(self):
        """Close the client connection."""
        self._logger.notice("Closing Tektronix AFG client")
        if self._requestSocket:
            self._requestSocket.close()
        if self._statusSocket:
            self._statusSocket.close() 