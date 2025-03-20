from plico.utils.decorator import override
from plico.utils.snapshotable import Snapshotable
import time
import json
from plico.utils.logger import Logger
from plico.rpc.zmq_ports import ZmqPorts
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico_io.utils.constants import Constants


class DriveStatus:
    """Drive status class to handle drive device status.
    
    This class provides methods to get and set the status of a drive device.
    """
    
    def __init__(self, name, is_on=False):
        """Create a drive status instance.
        
        Parameters
        ----------
        name : str
            Name of the drive device
        is_on : bool, optional
            Whether the drive is on, default is False
        """
        self._name = name
        self._is_on = is_on
        self._logger = Logger.of(name)
        
    def is_on(self):
        """Get whether the drive is on.
        
        Returns
        -------
        bool
            True if the drive is on, False otherwise
        """
        return self._is_on
        
    def set_on(self, is_on):
        """Set whether the drive is on.
        
        Parameters
        ----------
        is_on : bool
            Whether the drive is on
        """
        self._is_on = is_on
        self._logger.notice(f"Drive {self._name} is now {'on' if is_on else 'off'}")
        
    def to_dict(self):
        """Convert the status to a dictionary.
        
        Returns
        -------
        dict
            Dictionary representation of the status
        """
        return {
            'name': self._name,
            'is_on': self._is_on
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create a drive status instance from a dictionary.
        
        Parameters
        ----------
        data : dict
            Dictionary representation of the status
            
        Returns
        -------
        DriveStatus
            A drive status instance
        """
        return cls(
            name=data['name'],
            is_on=data['is_on']
        )


class ControllerStatus(Snapshotable):
    """Status of the controller device.

    Contains all the information about the state of the controller.
    """

    def __init__(self, devices=None, connected=False):
        """Create a ControllerStatus object.

        Parameters
        ----------
        devices: dict
            Dictionary of devices connected to the controller
        connected: bool
            Whether the controller is connected to the devices
        """
        self._devices = devices if devices is not None else {}
        self._connected = connected

    @property
    def devices(self):
        """Return the devices dictionary."""
        return self._devices

    @property
    def connected(self):
        """Return whether the controller is connected."""
        return self._connected

    @override
    def as_dict(self):
        """Return a dictionary representation of the status."""
        return {
            'devices': self._devices,
            'connected': self._connected,
        } 