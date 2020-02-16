# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)

import os
import re
import subprocess


# Get environment name
environment = None

if os.path.isfile('.ploy'):
    # Read environment name from .ploy (without PyYAML)
    with open('.ploy', 'r') as f:
        yaml = f.read()
        
    match = re.search('environment:[\s]*(.*)[\r\n]*', yaml)
    environment = match.group(1)

if environment is None:
    environment = '.venv'


# Create a virtual environment in .venv
subprocess.check_call(['python', '-m', 'venv', environment])

# Install requirements.txt
subprocess.check_call([environment + '/bin/python', '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([environment + '/bin/python', '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Run gitploy.py with 
subprocess.check_call([environment + '/bin/python', 'gitploy.py'])

