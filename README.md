# Port Monitor

Port Monitor is a configurable tool for monitoring network ports and sending alerts through various channels. It provides a flexible solution for system administrators and network security professionals to keep track of port activity and receive timely notifications.

## Features

- Monitor multiple network ports
- Configurable alert thresholds
- Multiple alert methods: Email, Webhook, Slack, Telegram, PagerDuty
- Rate limiting for alerts to prevent alert fatigue
- CSV export of connection history for further analysis

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/jameschrisa/port_monitor.git
cd port_monitor
```

### Step 2: Set Up the Project

Choose one of the following options:

#### Option A: Using the Initialization Script (Recommended for Developers)

1. Run the initialization script:
   ```bash
   python init_project.py
   ```
   This script creates the necessary directory structure and files, including `__init__.py`.

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

#### Option B: Direct Installation (Quickest for Users)

1. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the package:
   ```bash
   pip install .
   ```

Note: The `setup.py` script automatically ensures that the `__init__.py` file exists during installation.

## Usage

After installation, use the following commands:

1. Configure the Port Monitor:
   ```bash
   configure_port_monitor
   ```
   Follow the prompts to set up your monitoring preferences and alert methods.

2. Run the Port Monitor:
   ```bash
   port_monitor
   ```

If these commands aren't recognized, try:

```bash
python -m port_monitor.configure_port_monitor
python -m port_monitor.port_monitor
```

## Configuration

The configuration process will guide you through setting up:

- Ports to monitor
- Alert thresholds
- Email notifications
- Webhook integrations
- Slack alerts
- Telegram notifications
- PagerDuty alerts
- Logging preferences
- CSV export options

You can rerun the configuration at any time using the `configure_port_monitor` command.

## Development

### Project Structure

```
port_monitor/
├── port_monitor/
│   ├── __init__.py
│   ├── port_monitor.py
│   └── configure_port_monitor.py
├── init_project.py
├── README.md
├── requirements.txt
└── setup.py
```

### Making Changes

1. Ensure you've installed the package in editable mode (`pip install -e .`).
2. Make changes to the Python files in the `port_monitor` directory.
3. Changes will be immediately reflected when running the commands.
4. For changes to `setup.py` or adding new files, reinstall the package.

### Testing

After making changes:

1. Run the configuration script:
   ```bash
   configure_port_monitor
   ```

2. Run the main script:
   ```bash
   port_monitor
   ```

3. Verify that your changes work as expected.

## Troubleshooting

- If commands are not found, ensure that your Python scripts directory is in your system's PATH.
- Verify that the package is installed correctly: `pip list | grep port_monitor`
- For permission issues, you may need to use `sudo` on Unix-based systems or run as administrator on Windows.
- If you encounter import errors, make sure the `__init__.py` file exists in the `port_monitor` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- List any libraries or tools that inspired or are used in this project
- Credit any contributors or sources of significant help

## Contact

Project Link: [https://github.com/jameschrisa/port_monitor](https://github.com/yourusername/port_monitor)
