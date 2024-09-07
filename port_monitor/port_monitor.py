import time
import logging
import os
import signal
import sys
import datetime
import yaml
import psutil
from collections import defaultdict
import csv

# For system tray icon (optional, requires additional setup)
try:
    import pystray
    from PIL import Image
    SYSTEM_TRAY_AVAILABLE = True
except ImportError:
    SYSTEM_TRAY_AVAILABLE = False

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Global variables
SHUTDOWN_FLAG = False
PID_FILE = 'port_monitor.pid'
CONFIG_FILE = 'port_monitor_config.yaml'

# Configure logging
logging.basicConfig(filename='port_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Store connection history
connection_history = defaultdict(list)

def create_pid_file():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def remove_pid_file():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = True
    print(f"\n{YELLOW}Received termination signal. Shutting down gracefully...{RESET}")
    logging.info("Received termination signal. Initiating graceful shutdown.")

def create_system_tray_icon():
    if not SYSTEM_TRAY_AVAILABLE:
        return None
    
    image = Image.new('RGB', (64, 64), color = (73, 109, 137))
    def exit_action(icon):
        icon.stop()
        global SHUTDOWN_FLAG
        SHUTDOWN_FLAG = True
    
    return pystray.Icon("Port Monitor", image, "Port Monitor", menu=pystray.Menu(
        pystray.MenuItem("Exit", exit_action)
    ))

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def check_ports():
    current_time = time.time()
    new_connections = 0
    try:
        for conn in psutil.net_connections(kind='inet'):
            if SHUTDOWN_FLAG:
                return new_connections
            try:
                if conn.laddr.port in config['ports_to_monitor']:
                    connection_key = (conn.laddr.port, conn.raddr.ip if conn.raddr else 'N/A')
                    connection_history[connection_key].append(current_time)
                    
                    # Remove old connections from history
                    connection_history[connection_key] = [t for t in connection_history[connection_key] if current_time - t <= 3600]
                    
                    conn_count = len(connection_history[connection_key])
                    if conn_count >= config['alert_levels']['critical']['threshold']:
                        alert_message = f"{RED}CRITICAL: {conn_count} connections detected on port {conn.laddr.port} from {conn.raddr.ip if conn.raddr else 'N/A'}{RESET}"
                        logging.critical(alert_message)
                        print(alert_message)
                    elif conn_count >= config['alert_levels']['warning']['threshold']:
                        alert_message = f"{YELLOW}WARNING: {conn_count} connections detected on port {conn.laddr.port} from {conn.raddr.ip if conn.raddr else 'N/A'}{RESET}"
                        logging.warning(alert_message)
                        print(alert_message)
                    new_connections += 1
            except psutil.AccessDenied:
                logging.debug(f"AccessDenied for a connection (likely a system process)")
            except Exception as e:
                logging.error(f"Unexpected error checking connection: {str(e)}")
    except psutil.AccessDenied:
        logging.warning("AccessDenied when trying to get net_connections. Trying again in next iteration.")
    except Exception as e:
        logging.error(f"Unexpected error in check_ports: {str(e)}")
    return new_connections

def export_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Port', 'Remote IP', 'Connection Count', 'Last Connection Time'])
        for (port, ip), times in connection_history.items():
            writer.writerow([port, ip, len(times), datetime.datetime.fromtimestamp(max(times)).strftime('%Y-%m-%d %H:%M:%S')])

def main():
    global SHUTDOWN_FLAG
    create_pid_file()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logging.info("Port monitoring started")
    print(f"{GREEN}Port monitoring started. Check port_monitor.log for updates.{RESET}")

    icon = create_system_tray_icon()
    if icon:
        icon.run_detached()

    spinner = spinning_cursor()
    start_time = time.time()
    connection_count = 0

    try:
        while not SHUTDOWN_FLAG:
            try:
                current_time = time.time()
                elapsed_time = current_time - start_time

                new_connections = check_ports()
                connection_count += new_connections

                # Update the spinner and status
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                sys.stdout.write('\b')

                # Print and log status update every 5 minutes
                if elapsed_time % 300 < config['monitoring']['check_interval']:
                    status_message = f"{YELLOW}[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Monitoring active. Total connections: {connection_count}{RESET}"
                    print(status_message)
                    logging.info(f"Monitoring active. Total connections: {connection_count}")

                time.sleep(config['monitoring']['check_interval'])
            except Exception as e:
                logging.error(f"An error occurred in the main loop: {str(e)}")
                print(f"{RED}An error occurred. Check the log for details.{RESET}")
                time.sleep(config['monitoring']['check_interval'])

    finally:
        logging.info("Port monitoring stopped")
        print(f"{GREEN}Port monitoring stopped.{RESET}")
        remove_pid_file()
        if icon:
            icon.stop()
        if config['export']['enabled']:
            export_to_csv(config['export']['file'])
            export_message = f"{GREEN}Connection history exported to {config['export']['file']}{RESET}"
            print(export_message)
            logging.info(f"Connection history exported to {config['export']['file']}")

if __name__ == "__main__":
    main()
