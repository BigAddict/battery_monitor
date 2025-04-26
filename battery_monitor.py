#!/usr/bin/env python3
"""
Battery Monitor - A cross-platform utility to monitor laptop battery and alert users
when the battery level falls below a specified threshold.

This script runs in the background and checks battery status at regular intervals.
It sends a system notification when the battery is low and not charging.
"""
from data_scrapping import log_battery_status
from pathlib import Path
import argparse
import platform
import logging
import psutil
import time
import json
import sys
import os

# Configure paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
LOG_DIR = BASE_DIR / "logs"

# Default configuration
DEFAULT_CONFIG = {
    "battery_threshold": 15,
    "check_interval": 60,
    "notification_repeat_delay": 300,  # 5 minutes
    "log_level": "INFO"
}

def setup_logging(log_level="INFO"):
    """Configure and set up logging"""
    # Create log directory if it doesn't exist
    LOG_DIR.mkdir(exist_ok=True)
    
    # Set log level
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    selected_level = log_level_map.get(log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=selected_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "battery_monitor.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def load_config():
    """Load or create configuration file"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
            return config
        except json.JSONDecodeError:
            logger.error(f"Invalid config file format. Using defaults.")
            return DEFAULT_CONFIG
    else:
        # Create default config file
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

def get_battery_status():
    """Get current battery percentage and charging status
    
    Returns:
        tuple: (battery_percent, is_plugged_in) or (None, None) if not available
    """
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return None, None
        
        percent = battery.percent
        plugged = battery.power_plugged
        
        return percent, plugged
    except Exception as e:
        logger.error(f"Error getting battery status: {e}")
        return None, None

def send_notification(title, message):
    """Send a notification based on the operating system
    
    Args:
        title (str): The notification title
        message (str): The notification message content
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=10, threaded=True)
            except ImportError:
                logger.warning("win10toast not installed. Using fallback notification method.")
                # Fallback using PowerShell (Windows 10+)
                ps_cmd = f'powershell -command "New-BurntToastNotification -Text \'{title}\', \'{message}\'"'
                os.system(ps_cmd)
        
        elif system == "Darwin":  # macOS
            os.system(f"""osascript -e 'display notification "{message}" with title "{title}"'""")
        
        elif system == "Linux":
            # Try multiple notification methods
            notification_methods = [
                f"""notify-send "{title}" "{message}" """,
                f"""zenity --notification --text="{title}: {message}" """,
                f"""kdialog --passivepopup "{message}" 10 --title "{title}" """
            ]
            
            for cmd in notification_methods:
                try:
                    exit_code = os.system(cmd + " >/dev/null 2>&1")
                    if exit_code == 0:
                        break
                except:
                    continue
        
        logger.info(f"Notification sent: {title} - {message}")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

def parse_arguments():
    """Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Battery Monitor - Alerts when battery is low")
    parser.add_argument("-t", "--threshold", type=int, help="Battery threshold percentage (1-99)")
    parser.add_argument("-i", "--interval", type=int, help="Check interval in seconds")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--create-config", action="store_true", help="Create default config file and exit")
    parser.add_argument("--test", action="store_true", help="Run in test mode (10s interval) 🚀")
    
    return parser.parse_args()

def main():
    """Main function to monitor battery and send alerts"""

    global logger
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Handle config file creation request
    if args.create_config:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"Default configuration file created at {CONFIG_PATH}")
        return
    
    # Load configuration
    config = load_config()

        # 👇 FOR TESTING: Force fast logging interval
    if args.test:
        print("[TEST MODE] Running in fast logging mode: every 10 seconds")
        config['check_interval'] = 10
    
    # Override with command line arguments if provided
    if args.threshold:
        if 1 <= args.threshold <= 99:
            config['battery_threshold'] = args.threshold
        else:
            print("Threshold must be between 1 and 99")
            return
            
    if args.interval:
        if args.interval >= 10:
            config['check_interval'] = args.interval
        else:
            print("Interval must be at least 10 seconds")
            return
    
    # Set up logging
    log_level = "DEBUG" if args.debug else config.get("log_level", "INFO")
    logger = setup_logging(log_level)
    
    # Extract configuration
    BATTERY_THRESHOLD = config['battery_threshold']
    CHECK_INTERVAL = config['check_interval']
    NOTIFICATION_REPEAT_DELAY = config['notification_repeat_delay']
    
    logger.info(f"Battery monitor started (threshold: {BATTERY_THRESHOLD}%, interval: {CHECK_INTERVAL}s)")
    
    send_notification("BigAddict", "A battery monitor has being started. Innovation at it's peek")
    
    # Keep track of alert state
    already_alerted = False
    last_alert_time = 0
    
    try:
        while True:
            percent, plugged = get_battery_status()
            
            if percent is None:
                logger.warning("Could not get battery information")
                time.sleep(CHECK_INTERVAL)
                continue
                
            logger.debug(f"Battery level: {percent}% - Plugged in: {plugged}")
            
            current_time = time.time()
            time_since_last_alert = current_time - last_alert_time
            
            # Alert if battery is below threshold and not plugged in
            if percent < BATTERY_THRESHOLD and not plugged:
                # Only send alert if we haven't already or enough time has passed since last alert
                if not already_alerted or time_since_last_alert > NOTIFICATION_REPEAT_DELAY:
                    send_notification(
                        "Low Battery Alert", 
                        f"Battery level is at {percent}%. Please connect charger."
                    )
                    already_alerted = True
                    last_alert_time = current_time
            # Reset alert flag when battery is charging or above threshold
            elif percent >= BATTERY_THRESHOLD or plugged:
                if already_alerted:
                    logger.debug("Alert condition cleared")
                already_alerted = False

            try:
                log_battery_status()
            except Exception as e:
                send_notification("Data Scrapping", f"Scrapping failed\n{e}")
                continue
                
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Battery monitor stopped by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
