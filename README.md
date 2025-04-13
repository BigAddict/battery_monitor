# Battery Monitor

A simple Python application that monitors your laptop battery level and alerts you when it drops below a specified threshold.

## Features

- Cross-platform support (Windows, macOS, Linux)
- System notifications when battery is low
- Configurable battery threshold and check interval
- JSON configuration file for easy customization
- Command-line options to override settings
- Repeated notifications with configurable delay
- Logging of battery events with customizable level
- Only alerts once until battery is charged above threshold or plugged in

## Requirements

- Python 3.6+
- psutil library
- For Windows: win10toast library (optional, fallback available)

## Installation

1. Clone this repository:
   ```
   git clone https://your-repository-url/battery_monitor.git
   cd battery_monitor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script manually:

```
python battery_monitor.py
```

### Command-line Options

```
python battery_monitor.py [-h] [-t THRESHOLD] [-i INTERVAL] [-d] [--create-config]

Options:
  -h, --help            Show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        Battery threshold percentage (1-99)
  -i INTERVAL, --interval INTERVAL
                        Check interval in seconds
  -d, --debug           Enable debug logging
  --create-config       Create default config file and exit
```

### Configuration

The script uses a JSON configuration file (`config.json`) in the same directory. It will be created automatically on first run with these default settings:

```json
{
    "battery_threshold": 15,
    "check_interval": 60,
    "notification_repeat_delay": 300,
    "log_level": "INFO"
}
```

You can modify these settings to customize the behavior:
- `battery_threshold`: Battery percentage level that triggers alerts (1-99)
- `check_interval`: Time in seconds between battery checks
- `notification_repeat_delay`: Time in seconds before repeating a notification if battery remains low
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Setting up to run automatically

#### Windows

Option 1: Using the provided batch file
1. Edit the `start_monitor.bat` file path if needed
2. Press `Win + R` and type `shell:startup`
3. Create a shortcut to `start_monitor.bat` in the startup folder

Option 2: Using Task Scheduler
1. Open Task Scheduler
2. Create a new task to run at login
3. Set the action to start program: `pythonw C:\path\to\battery_monitor.py`

#### macOS

1. Edit the `com.user.batterymonitor.plist` file, replacing `%ABSOLUTE_PATH%` with the actual path
2. Copy the plist file to `~/Library/LaunchAgents/`
3. Load the agent:
   ```
   launchctl load ~/Library/LaunchAgents/com.user.batterymonitor.plist
   ```

#### Linux

1. Edit the `battery-monitor.desktop` file, replacing `%ABSOLUTE_PATH%` with the actual path
2. Copy to `~/.config/autostart/`
   ```
   cp battery-monitor.desktop ~/.config/autostart/
   ```

## Logs

Logs are stored in the `logs` directory and contain information about battery levels and notification events. The default log level is INFO, but you can change it in the config file or use the `-d` flag for debug output.
