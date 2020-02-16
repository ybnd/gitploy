import os
import shutil


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
    
    
# Remove virtual environment
if os.path.isdir('.venv'):
    shutil.rmtree('.venv')

# Remove .git
if os.path.isdir('.git'):
    shutil.rmtree('.git')

