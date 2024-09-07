![portmon](./portmon.png "portmon")
# SIEM Port Monitor Lite

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

If you encounter issues during installation or usage of Port Monitor, try the following steps:

### Installation Issues

1. **Upgrade pip**: 
   Ensure you have the latest version of pip:
   ```
   python -m pip install --upgrade pip
   ```

2. **Install Cython**:
   Some dependencies might require Cython. Install it before proceeding:
   ```
   pip install Cython
   ```

3. **Use pre-built wheels**:
   If building from source fails, try using pre-built wheels:
   ```
   pip install --only-binary=:all: PyYAML
   pip install .
   ```

4. **Install PyYAML without Cython**:
   If PyYAML is causing issues, try installing it without Cython:
   ```
   PYYAML_FORCE_LIBYAML=1 pip install PyYAML
   pip install .
   ```

5. **Check Python compatibility**:
   Ensure your Python version is compatible with the package requirements. This project supports Python 3.6+.

6. **Install build tools**:
   On macOS, you might need to install Xcode Command Line Tools:
   ```
   xcode-select --install
   ```

7. **Use editable mode**:
   For development, try installing in editable mode with verbose output:
   ```
   pip install -e . -v
   ```

### Dependency Conflicts

If you encounter dependency conflicts, try the following:

1. Check your installed packages:
   ```
   pip list
   ```

2. Ensure the versions in `requirements.txt` and `setup.py` are compatible with your installed packages.

3. If needed, update the version requirements to be more flexible. For example, change:
   ```
   PyYAML==5.4.1
   ```
   to
   ```
   PyYAML>=5.4.1
   ```

### Still Having Issues?

If you're still experiencing problems after trying these steps, please open an issue on the GitHub repository with the following information:

1. Your Python version (`python --version`)
2. Your pip version (`pip --version`)
3. The content of your `pip list` output
4. The full error message you're encountering
5. The contents of your `setup.py` and `requirements.txt` files

This information will help in diagnosing and resolving the issue more quickly.

## Contributing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- List any libraries or tools that inspired or are used in this project
- Credit any contributors or sources of significant help

## Contact

Project Link: [https://github.com/jameschrisa/port_monitor](https://github.com/yourusername/port_monitor)
