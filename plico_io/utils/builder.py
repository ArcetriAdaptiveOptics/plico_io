#!/usr/bin/env python

from plico.utils.snapshotable import Snapshotable
from plico.utils.logger import Logger
from plico_io.client.controller_client import ControllerClient
from plico_io.utils.constants import Constants
import ast
import six


class DriveClientBuilder(Snapshotable):
    """Builder for the drive client."""

    def __init__(self, logger=None):
        """Create a DriveClientBuilder instance.

        Parameters
        ----------
        logger : Logger, optional
            A logger for the builder
        """
        self._logger = logger or Logger.of('Drive Client Builder')
        self._host = None
        self._port = None
        self._snapshot = None

    def host(self, host_name):
        """Set the host name.

        Parameters
        ----------
        host_name : str
            The name of the host where the server is running

        Returns
        -------
        DriveClientBuilder
            This builder instance
        """
        self._host = host_name
        return self

    def port(self, port_number):
        """Set the port number.

        Parameters
        ----------
        port_number : int
            The port number for the server connection

        Returns
        -------
        DriveClientBuilder
            This builder instance
        """
        self._port = port_number
        return self

    def from_configuration(self, configuration, section_name=None):
        """Configure the builder from a configuration instance.

        Parameters
        ----------
        configuration : plico.utils.Configuration
            The configuration to use
        section_name : str, optional
            The configuration section to use. If not provided, the default section is used.

        Returns
        -------
        DriveClientBuilder
            This builder instance
        """
        section = section_name or Constants.DEFAULT_DRIVE_SECTION

        try:
            host = configuration.getValue(section, 'host')
            port = configuration.getValue(section, 'port', getint=True)
            self.host(host).port(port)
        except Exception as e:
            self._logger.error(f"Cannot parse configuration: {str(e)}")
            raise

        return self

    def build(self):
        """Build a DriveClient with the specified configuration.

        Returns
        -------
        ControllerClient
            The constructed DriveClient
        """
        assert self._host is not None, "Host must be specified"
        assert self._port is not None, "Port must be specified"

        return ControllerClient(self._host, self._port)

    def getSnapshot(self):
        """Get the snapshot of the builder.

        Returns
        -------
        dict
            The snapshot of the builder
        """
        return {
            'host': self._host,
            'port': self._port
        }


# For backward compatibility
DriveBuilder = DriveClientBuilder 