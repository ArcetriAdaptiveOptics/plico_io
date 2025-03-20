from abc import ABC, abstractmethod
import time
import json
from plico.utils.logger import Logger
from plico.rpc.zmq_ports import ZmqPorts
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico_io.utils.constants import Constants


class AbstractControllerClient(ABC):
    """Abstract base class for all controller clients.
    
    This defines the interface that all controller clients must implement.
    """

    @abstractmethod
    def turn_on(self, device_id=None, channel=0, timeout_in_sec=None):
        """Turn on a device.
        
        Parameters
        ----------
        device_id : str or None
            The ID of the device to turn on. If None, use the first available device.
        channel : int
            The channel to turn on (default: 0)
        timeout_in_sec : float
            Timeout in seconds for the operation
        
        Returns
        -------
        bool
            True if operation was successful
        """
        pass

    @abstractmethod
    def turn_off(self, device_id=None, channel=0, timeout_in_sec=None):
        """Turn off a device.
        
        Parameters
        ----------
        device_id : str or None
            The ID of the device to turn off. If None, use the first available device.
        channel : int
            The channel to turn off (default: 0)
        timeout_in_sec : float
            Timeout in seconds for the operation
            
        Returns
        -------
        bool
            True if operation was successful
        """
        pass

    @abstractmethod
    def get_status(self, device_id=None, channel=0, timeout_in_sec=None):
        """Get the current status of a device.
        
        Parameters
        ----------
        device_id : str or None
            The ID of the device to check. If None, use the first available device.
        channel : int
            The channel to check (default: 0)
        timeout_in_sec : float
            Timeout in seconds for the operation
            
        Returns
        -------
        dict
            Status information about the device
        """
        pass

    @abstractmethod
    def list_devices(self, timeout_in_sec=None):
        """List all available devices.
        
        Parameters
        ----------
        timeout_in_sec : float
            Timeout in seconds for the operation
            
        Returns
        -------
        dict
            A dictionary of available devices with their IDs as keys
        """
        pass

    @abstractmethod
    def get_snapshot(self, timeout_in_sec=None):
        """Get a snapshot of the controller state.
        
        Parameters
        ----------
        timeout_in_sec : float
            Timeout in seconds for the operation
            
        Returns
        -------
        dict
            Snapshot information about the controller state
        """
        pass

    @abstractmethod
    def close(self):
        """Close the client connection."""
        pass 