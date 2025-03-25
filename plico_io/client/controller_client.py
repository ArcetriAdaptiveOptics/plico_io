import time
import json
from plico.utils.logger import Logger
from plico.rpc.zmq_ports import ZmqPorts
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico_io.utils.constants import Constants
from plico_io.client.abstract_controller_client import AbstractControllerClient
from plico_io.utils.timeout import Timeout


class ControllerClient(AbstractControllerClient):
    """Controller client class for interacting with Meross controller devices.
    
    This class provides methods to control Meross smart plugs through
    the PLICO controller server.
    """
    
    def __init__(self, host, port, name=None):
        """Create a controller client instance.
        
        Parameters
        ----------
        host : str
            Hostname or IP address of the controller server
        port : int
            Port number of the controller server
        name : str, optional
            Name of the controller client instance, by default None
        """
        self._name = name or f"Controller-{host}:{port}"
        self._host = host
        self._port = port
        self._logger = Logger.of(self._name)
        
        # Initialize RPC
        self._rpc = ZmqRemoteProcedureCall()
        
        # Initialize sockets
        self._requestSocket = self._rpc.requestSocket(self._host, self._port)
        self._statusSocket = None  # Status socket is optional
        
        self._logger.notice(f"Controller client initialized for {host}:{port}")
        
    def turn_on(self, device_id=None, channel=0, timeout_in_sec=Timeout.SETTER):
        """Turn on a device.
        
        Parameters
        ----------
        device_id : str, optional
            ID of the device to turn on, by default None (use first available)
        channel : int, optional
            Channel number to turn on, by default 0
        timeout_in_sec : float, optional
            Timeout in seconds, by default Timeout.SETTER
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        self._logger.notice(f"Turning on device {device_id}, channel {channel}")
        return self._rpc.sendRequest(self._requestSocket, 'turnOn', timeout=timeout_in_sec)
        
    def turn_off(self, device_id=None, channel=0, timeout_in_sec=Timeout.SETTER):
        """Turn off a device.
        
        Parameters
        ----------
        device_id : str, optional
            ID of the device to turn off, by default None (use first available)
        channel : int, optional
            Channel number to turn off, by default 0
        timeout_in_sec : float, optional
            Timeout in seconds, by default Timeout.SETTER
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        self._logger.notice(f"Turning off device {device_id}, channel {channel}")
        return self._rpc.sendRequest(self._requestSocket, 'turnOff', timeout=timeout_in_sec)
        
    def get_status(self, device_id=None, channel=0, timeout_in_sec=Timeout.GETTER):
        """Get the status of a device.
        
        Parameters
        ----------
        device_id : str, optional
            ID of the device to check, by default None (use first available)
        channel : int, optional
            Channel number to check, by default 0
        timeout_in_sec : float, optional
            Timeout in seconds, by default Timeout.GETTER
            
        Returns
        -------
        dict
            Status information
        """
        self._logger.debug("Getting status")
        return self._rpc.sendRequest(self._requestSocket, 'getStatus', timeout=timeout_in_sec)
        
    def list_devices(self, timeout_in_sec=Timeout.GETTER):
        """List all available devices.
        
        Parameters
        ----------
        timeout_in_sec : float, optional
            Timeout in seconds, by default Timeout.GETTER
            
        Returns
        -------
        dict
            Dictionary of devices
        """
        self._logger.debug("Listing devices")
        status = self._rpc.sendRequest(self._requestSocket, 'getStatus', timeout=timeout_in_sec)
        return status.get('devices', {})
        
    def get_snapshot(self, timeout_in_sec=Timeout.GETTER):
        """Get a snapshot of the controller state.
        
        Parameters
        ----------
        timeout_in_sec : float, optional
            Timeout in seconds, by default Timeout.GETTER
            
        Returns
        -------
        dict
            Snapshot information
        """
        self._logger.debug("Getting snapshot")
        return self._rpc.sendRequest(self._requestSocket, 'getSnapshot', timeout=timeout_in_sec)
        
    def close(self):
        """Close the client connection."""
        self._logger.notice("Closing controller client")
        if self._requestSocket:
            self._requestSocket.close()
        if self._statusSocket:
            self._statusSocket.close() 