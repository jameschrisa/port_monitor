import os
import sys

def initialize_project():
    # Create the main package directory
    os.makedirs('port_monitor', exist_ok=True)

    # Create __init__.py
    init_path = os.path.join('port_monitor', '__init__.py')
    open(init_path, 'a').close()

    # Create other necessary files if they don't exist
    files_to_create = [
        ('port_monitor', 'port_monitor.py'),
        ('port_monitor', 'configure_port_monitor.py'),
        'requirements.txt',
        'setup.py',
        'README.md'
    ]

    for file_path in files_to_create:
        if isinstance(file_path, tuple):
            file_path = os.path.join(*file_path)
        if not os.path.exists(file_path):
            open(file_path, 'a').close()
            print(f"Created: {file_path}")

    print("Project structure initialized successfully.")

if __name__ == "__main__":
    initialize_project()
