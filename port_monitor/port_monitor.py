import psutil
import time
import logging
from collections import defaultdict
import argparse
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import requests
import yaml
import os
import sys

def load_config(config_file):
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please create and configure the YAML file before running the script.")
        sys.exit(1)
    
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

CONFIG_FILE = 'port_monitor_config.yaml'
config = load_config(CONFIG_FILE)

# Set up logging
logging.basicConfig(filename=config['logging']['file'], level=config['logging']['level'],
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

PORTS_TO_MONITOR = config['ports_to_monitor']

# Store connection history
connection_history = defaultdict(list)

# Store alert history for rate limiting
alert_history = []

def send_email_alert(subject, body):
    if not config['alerts']['email']['enabled']:
        return
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['alerts']['email']['from_email']
    msg['To'] = config['alerts']['email']['to_email']

    try:
        with smtplib.SMTP(config['alerts']['email']['smtp_server'], config['alerts']['email']['smtp_port']) as server:
            server.starttls()
            server.login(config['alerts']['email']['username'], config['alerts']['email']['password'])
            server.send_message(msg)
        logging.info("Email alert sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")

def send_webhook_alert(data):
    if not config['alerts']['webhook']['enabled']:
        return
    
    try:
        response = requests.post(config['alerts']['webhook']['url'], json=data)
        response.raise_for_status()
        logging.info("Webhook alert sent successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send webhook alert: {str(e)}")

def send_slack_alert(message):
    if not config['alerts']['slack']['enabled']:
        return
    
    try:
        response = requests.post(config['alerts']['slack']['webhook_url'], json={"text": message})
        response.raise_for_status()
        logging.info("Slack alert sent successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Slack alert: {str(e)}")

def send_telegram_alert(message):
    if not config['alerts']['telegram']['enabled']:
        return
    
    try:
        url = f"https://api.telegram.org/bot{config['alerts']['telegram']['bot_token']}/sendMessage"
        data = {"chat_id": config['alerts']['telegram']['chat_id'], "text": message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info("Telegram alert sent successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram alert: {str(e)}")

def send_pagerduty_alert(message):
    if not config['alerts']['pagerduty']['enabled']:
        return
    
    try:
        url = "https://events.pagerduty.com/v2/enqueue"
        data = {
            "routing_key": config['alerts']['pagerduty']['integration_key'],
            "event_action": "trigger",
            "payload": {
                "summary": message,
                "severity": "critical",
                "source": "Port Monitor Script"
            }
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.info("PagerDuty alert sent successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send PagerDuty alert: {str(e)}")

def send_alert(level, message):
    current_time = time.time()
    alert_history.append(current_time)
    alert_history[:] = [t for t in alert_history if current_time - t <= 3600]
    
    if len(alert_history) > config['rate_limiting']['max_alerts_per_hour']:
        logging.warning("Alert rate limit exceeded. Skipping this alert.")
        return
    
    send_email_alert(f"Port Monitor {level.capitalize()} Alert", message)
    send_webhook_alert({"level": level, "message": message})
    send_slack_alert(f"{level.upper()}: {message}")
    send_telegram_alert(f"{level.upper()}: {message}")
    send_pagerduty_alert(message)

def check_ports():
    current_time = time.time()
    for conn in psutil.net_connections():
        if conn.laddr.port in PORTS_TO_MONITOR:
            connection_key = (conn.laddr.port, conn.raddr.ip if conn.raddr else 'N/A')
            connection_history[connection_key].append(current_time)
            
            # Remove old connections from history
            connection_history[connection_key] = [t for t in connection_history[connection_key] if current_time - t <= 3600]
            
            conn_count = len(connection_history[connection_key])
            if conn_count >= config['alert_levels']['critical']['threshold']:
                alert_message = f"CRITICAL: {conn_count} connections detected on port {conn.laddr.port} from {conn.raddr.ip if conn.raddr else 'N/A'}"
                log_connection(conn, alert_message)
                send_alert("critical", alert_message)
            elif conn_count >= config['alert_levels']['warning']['threshold']:
                alert_message = f"WARNING: {conn_count} connections detected on port {conn.laddr.port} from {conn.raddr.ip if conn.raddr else 'N/A'}"
                log_connection(conn, alert_message)
                send_alert("warning", alert_message)
            else:
                log_connection(conn, "Connection detected")

def log_connection(conn, message):
    log_message = f"{message} on port {conn.laddr.port}\n" \
                  f"Local address: {conn.laddr.ip}:{conn.laddr.port}\n" \
                  f"Remote address: {conn.raddr.ip if conn.raddr else 'N/A'}:{conn.raddr.port if conn.raddr else 'N/A'}\n" \
                  f"Status: {conn.status}\n" \
                  f"PID: {conn.pid}\n" \
                  f"Process name: {psutil.Process(conn.pid).name() if conn.pid else 'N/A'}"
    logging.info(log_message)
    print(log_message)

def export_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Port', 'Remote IP', 'Connection Count', 'Last Connection Time'])
        for (port, ip), times in connection_history.items():
            writer.writerow([port, ip, len(times), datetime.fromtimestamp(max(times)).strftime('%Y-%m-%d %H:%M:%S')])

def main():
    print(f"Starting port monitoring (Interval: {config['monitoring']['check_interval']}s, Alert Threshold: {config['monitoring']['alert_threshold']} connections/hour)...")
    try:
        while True:
            check_ports()
            time.sleep(config['monitoring']['check_interval'])
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        if config['export']['enabled']:
            export_to_csv(config['export']['file'])
            print(f"Connection history exported to {config['export']['file']}")

if __name__ == "__main__":
    main()
