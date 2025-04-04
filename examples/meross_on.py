#!/usr/bin/env python
"""
Simple script to turn off the Meross device.
This script connects to the PLICO Meross controller server and turns off the device.
"""

import sys
import time
import argparse
from plico.utils.config_file_manager import ConfigFileManager
from plico.utils.configuration import Configuration
from plico_io.client.controller_client import ControllerClient
from plico_io.utils.builder import DriveClientBuilder


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Turn off PLICO drive controller')
    parser.add_argument('--config', 
                        type=str, 
                        help='Path to configuration file',
                        default=None)
    parser.add_argument('--section', 
                        type=str,
                        help='Configuration section name',
                        default='controller1')
    parser.add_argument('--host',
                        type=str,
                        help='Controller host',
                        default='localhost')
    parser.add_argument('--port',
                        type=int,
                        help='Controller port',
                        default=5010)
    return parser.parse_args()


def main():
    """Main function to turn off the controller."""
    args = parse_arguments()
    
    # Get configuration file
    if args.config:
        config_file = args.config
    else:
        # Use default configuration
        config_mgr = ConfigFileManager('inaf.arcetri.ao.plico_io_server',
                                      'INAF Arcetri Adaptive Optics',
                                      'plico_io_server')
        config_file = config_mgr.getConfigFilePath()
    
    # Create configuration
    config = Configuration()
    config.load(config_file)
    print(f"Using configuration file: {config_file}")
    
    # Create client
    try:
        print(f"Creating client for section: {args.section}")
        
        # Try to create from configuration first
        try:
            builder = DriveClientBuilder()
            client = builder.from_configuration(config, args.section).build()
            print("Client created from configuration")
        except Exception as e:
            print(f"Failed to create client from configuration: {str(e)}")
            print(f"Falling back to direct creation with host={args.host}, port={args.port}")
            builder = DriveClientBuilder()
            client = builder.host(args.host).port(args.port).build()
            print("Client created with direct parameters")
        
        # Check status before turning on
        print("Getting initial status...")
        status = client.get_status()
        print(f"Initial status: {status}")
        
        # Turn on the device
        print("Turning on the device...")
        result = client.turn_on()
        print(f"Turn off result: {result}")
        
        # Wait a moment to let the command process
        time.sleep(1)
        
        # Check status after turning off
        print("Getting updated status...")
        status = client.get_status()
        print(f"Updated status: {status}")
        
        print("\nDevice turned off successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 