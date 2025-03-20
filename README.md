# PLICO IO Client

A Python package for controlling IO devices through the PLICO framework. This package provides a client interface for interacting with various IO devices (like Meross smart plugs) through a PLICO server.

## Installation

```bash
pip install plico_io
```

## Configuration

The package uses a configuration file to store device settings. The default configuration file is located at:
- Windows: `%LOCALAPPDATA%\INAF Arcetri Adaptive Optics\inaf.arcetri.ao.plico_io_server\plico_io_server.conf`
- Linux/Mac: `~/.local/share/inaf.arcetri.ao.plico_io_server/plico_io_server.conf`

Example configuration file:
```ini
[controller1]
host = localhost
port = 5010
```

## Usage

### Creating a Client

```python
from plico_io.client.controller_client import ControllerClient
from plico_io.utils.builder import DriveClientBuilder

# Using the builder pattern (recommended)
builder = DriveClientBuilder()
client = builder.host('localhost').port(5010).build()

# Or from configuration
from plico.utils.configuration import Configuration
config = Configuration()
config.load('path/to/config.conf')
client = builder.from_configuration(config, 'controller1').build()
```

### Basic Operations

```python
# Get device status
status = client.get_status()
print(f"Device status: {status}")

# Turn device on
client.turn_on()

# Turn device off
client.turn_off()

# List available devices
devices = client.list_devices()
print(f"Available devices: {devices}")

# Get a snapshot of the controller state
snapshot = client.get_snapshot()
print(f"Controller snapshot: {snapshot}")

# Close the client when done
client.close()
```

### Command Line Tools

The package includes a command-line tool for basic operations:

```bash
# List available devices
plico_io_client --list

# Turn device on
plico_io_client --on

# Turn device off
plico_io_client --off

# Get device status
plico_io_client --status
```

## Examples

See the `examples` directory for more detailed examples:
- `simple_client.py`: Basic client usage
- `meross_client_test.py`: Testing Meross device functionality
- `meross_client_pulse.py`: Creating a pulse pattern with a device 