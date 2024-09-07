import yaml
import os
import sys
import getpass

CONFIG_FILE = 'port_monitor_config.yaml'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return yaml.safe_load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def get_input(prompt, default=None):
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()

def get_bool_input(prompt, default=None):
    while True:
        if default is not None:
            response = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
            if not response:
                return default
        else:
            response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'.")

def configure_ports(config):
    default_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389]
    current_ports = config.get('ports_to_monitor', default_ports)
    print("Current ports to monitor:", current_ports)
    
    if get_bool_input("Do you want to modify the list of ports to monitor?"):
        new_ports_input = input("Enter the ports to monitor (comma-separated), or press Enter to keep current ports: ").strip()
        if new_ports_input:
            new_ports = [int(port.strip()) for port in new_ports_input.split(',') if port.strip()]
            if new_ports:
                config['ports_to_monitor'] = new_ports
            else:
                print("No valid ports entered. Keeping current ports.")
        else:
            print("Keeping current ports.")
    else:
        config['ports_to_monitor'] = current_ports
    
    print("Ports to monitor:", config['ports_to_monitor'])

def configure_monitoring(config):
    monitoring = config.get('monitoring', {})
    monitoring['check_interval'] = int(get_input("Enter check interval in seconds", monitoring.get('check_interval', 60)))
    monitoring['alert_threshold'] = int(get_input("Enter alert threshold (connections per hour)", monitoring.get('alert_threshold', 5)))
    config['monitoring'] = monitoring

def configure_email_alerts(config):
    email = config.get('alerts', {}).get('email', {})
    email['enabled'] = get_bool_input("Enable email alerts?", email.get('enabled', False))
    if email['enabled']:
        email['smtp_server'] = get_input("SMTP server", email.get('smtp_server'))
        email['smtp_port'] = int(get_input("SMTP port", email.get('smtp_port', 587)))
        email['username'] = get_input("SMTP username", email.get('username'))
        email['password'] = getpass.getpass("SMTP password: ")
        email['from_email'] = get_input("From email", email.get('from_email'))
        email['to_email'] = get_input("To email", email.get('to_email'))
    config.setdefault('alerts', {})['email'] = email

def configure_webhook_alerts(config):
    webhook = config.get('alerts', {}).get('webhook', {})
    webhook['enabled'] = get_bool_input("Enable webhook alerts?", webhook.get('enabled', False))
    if webhook['enabled']:
        webhook['url'] = get_input("Webhook URL", webhook.get('url'))
    config.setdefault('alerts', {})['webhook'] = webhook

def configure_slack_alerts(config):
    slack = config.get('alerts', {}).get('slack', {})
    slack['enabled'] = get_bool_input("Enable Slack alerts?", slack.get('enabled', False))
    if slack['enabled']:
        slack['webhook_url'] = get_input("Slack webhook URL", slack.get('webhook_url'))
    config.setdefault('alerts', {})['slack'] = slack

def configure_telegram_alerts(config):
    telegram = config.get('alerts', {}).get('telegram', {})
    telegram['enabled'] = get_bool_input("Enable Telegram alerts?", telegram.get('enabled', False))
    if telegram['enabled']:
        telegram['bot_token'] = get_input("Telegram bot token", telegram.get('bot_token'))
        telegram['chat_id'] = get_input("Telegram chat ID", telegram.get('chat_id'))
    config.setdefault('alerts', {})['telegram'] = telegram

def configure_pagerduty_alerts(config):
    pagerduty = config.get('alerts', {}).get('pagerduty', {})
    pagerduty['enabled'] = get_bool_input("Enable PagerDuty alerts?", pagerduty.get('enabled', False))
    if pagerduty['enabled']:
        pagerduty['integration_key'] = get_input("PagerDuty integration key", pagerduty.get('integration_key'))
    config.setdefault('alerts', {})['pagerduty'] = pagerduty

def configure_logging(config):
    logging = config.get('logging', {})
    logging['file'] = get_input("Log file name", logging.get('file', 'port_monitor.log'))
    logging['level'] = get_input("Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", logging.get('level', 'INFO')).upper()
    config['logging'] = logging

def configure_export(config):
    export = config.get('export', {})
    export['enabled'] = get_bool_input("Enable CSV export?", export.get('enabled', False))
    if export['enabled']:
        export['file'] = get_input("Export file name", export.get('file', 'connection_history.csv'))
    config['export'] = export

def configure_rate_limiting(config):
    rate_limiting = config.get('rate_limiting', {})
    rate_limiting['max_alerts_per_hour'] = int(get_input("Maximum alerts per hour", rate_limiting.get('max_alerts_per_hour', 10)))
    config['rate_limiting'] = rate_limiting

def configure_alert_levels(config):
    alert_levels = config.get('alert_levels', {})
    alert_levels['warning'] = {'threshold': int(get_input("Warning threshold", alert_levels.get('warning', {}).get('threshold', 5)))}
    alert_levels['critical'] = {'threshold': int(get_input("Critical threshold", alert_levels.get('critical', {}).get('threshold', 10)))}
    config['alert_levels'] = alert_levels

def main():
    print("Port Monitor Configuration")
    print("==========================")
    
    config = load_config()
    
    configure_ports(config)
    configure_monitoring(config)
    configure_email_alerts(config)
    configure_webhook_alerts(config)
    configure_slack_alerts(config)
    configure_telegram_alerts(config)
    configure_pagerduty_alerts(config)
    configure_logging(config)
    configure_export(config)
    configure_rate_limiting(config)
    configure_alert_levels(config)
    
    save_config(config)
    print(f"\nConfiguration saved to {CONFIG_FILE}")

if __name__ == "__main__":
    main()
