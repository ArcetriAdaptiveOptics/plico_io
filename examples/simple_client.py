#!/usr/bin/env python
import time
import argparse
from plico.utils.logger import Logger
from plico_drive.client.drive_client import DriveClient
from plico_drive.utils.builder import DriveClientBuilder


def _parse_args():
    parser = argparse.ArgumentParser(description='Example client for PLICO drive server')
    parser.add_argument('--host', type=str, default='localhost',
                      help='Host running the drive server')
    parser.add_argument('--port', type=int, default=7100,
                      help='Port for the drive server')
    return parser.parse_args()


def main():
    args = _parse_args()
    logger = Logger.of('DriveClientExample')
    
    # Create a drive client using the builder
    builder = DriveClientBuilder()
    client = builder.host(args.host).port(args.port).build()
    
    try:
        # Example of using the drive client
        logger.notice("Connecting to drive server...")
        
        # Get initial status
        status = client.get_status()
        logger.notice(f"Initial drive status: {status.to_dict()}")
        
        # Turn the drive on
        logger.notice("Turning drive on...")
        client.set_on(True)
        time.sleep(1)  # Wait for status to update
        
        # Get updated status
        status = client.get_status()
        logger.notice(f"Updated drive status: {status.to_dict()}")
        
        # Turn the drive off
        logger.notice("Turning drive off...")
        client.set_on(False)
        time.sleep(1)  # Wait for status to update
        
        # Get final status
        status = client.get_status()
        logger.notice(f"Final drive status: {status.to_dict()}")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        # Clean up
        client.close()
        logger.notice("Client closed")


if __name__ == '__main__':
    main() 