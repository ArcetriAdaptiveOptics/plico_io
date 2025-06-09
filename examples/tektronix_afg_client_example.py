#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example client for Tektronix AFG server.

This script demonstrates how to connect to the Tektronix AFG server
and control the waveform generator using the `TektronixAFGClient`.

__author__ = "Marco Bonaglia"
__version__ = "1.0.0"
__date__ = "2025-06-09"
"""

import time
import argparse
from plico.utils.logger import Logger
from plico_io.tektronix_afg.client.tektronix_afg_client import TektronixAFGClient
from plico_io.utils.timeout import Timeout


def _parse_args():
    parser = argparse.ArgumentParser(description='Example client for Tektronix AFG server')
    parser.add_argument('--host', type=str, default='localhost',
                      help='Host running the Tektronix AFG server')
    parser.add_argument('--port', type=int, default=7100,
                      help='Port for the Tektronix AFG server')
    return parser.parse_args()


def main():
    args = _parse_args()
    logger = Logger.of('TektronixAFGClientExample')
    
    client = TektronixAFGClient(host=args.host, port=args.port)
    
    try:
        logger.notice("Connecting to Tektronix AFG server...")
        
        # Example of using the Tektronix AFG client
        logger.notice("Listing devices (channels):")
        devices = client.list_devices()
        for device_id, info in devices.items():
            logger.notice(f"  Device ID: {device_id}, Name: {info['name']}, Type: {info['type']}")

        logger.notice("Turning on Channel 1 and setting a sine wave...")
        client.set_function(channel=1, function="SIN")
        client.set_frequency(channel=1, frequency=1000, unit="Hz")
        client.set_amplitude(channel=1, amplitude=2.0, unit="Vpp")
        client.set_offset(channel=1, offset=0.0, unit="V")
        client.set_output(channel=1, state="ON")
        time.sleep(1)  # Wait for status to update
        
        logger.notice("Getting status for Channel 1...")
        ch1_status = client.get_status(channel=1)
        logger.notice(f"Channel 1 output status: {"ON" if ch1_status else "OFF"}")

        logger.notice("Turning on Channel 2 and setting a square wave...")
        client.set_function(channel=2, function="SQU")
        client.set_frequency(channel=2, frequency=500, unit="Hz")
        client.set_amplitude(channel=2, amplitude=5.0, unit="Vpp")
        client.set_offset(channel=2, offset=1.0, unit="V")
        client.set_output(channel=2, state="ON")
        time.sleep(1)

        logger.notice("Getting status for Channel 2...")
        ch2_status = client.get_status(channel=2)
        logger.notice(f"Channel 2 output status: {"ON" if ch2_status else "OFF"}")

        logger.notice("Printing all settings from the server...")
        client.print_settings()

        logger.notice("Turning off Channel 1...")
        client.turn_off(channel=1)
        time.sleep(1)

        logger.notice("Getting status for Channel 1 again...")
        ch1_status = client.get_status(channel=1)
        logger.notice(f"Channel 1 output status: {"ON" if ch1_status else "OFF"}")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        client.close()
        logger.notice("Client closed")


if __name__ == '__main__':
    main() 