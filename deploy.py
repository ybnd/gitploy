# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)

import os
import re
import subprocess


gitploy = '''# Bootstrap .git connection with dulwich

import os
from dulwich import porcelain
import yaml


cwd = os.getcwd()

if os.path.isfile('.ploy'):
    with open('.ploy', 'r') as f:
        ploy = yaml.safe_load(f.read())

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = porcelain.open_repo(cwd)
else:
    print(f"Cloning remote repository from {ploy['url']} to {cwd}")
    repo = porcelain.clone(ploy['url'] ,cwd)

fetched_data = porcelain.fetch(repo, ploy['url'])
'''


# Change working directory if called from scripts/
og_cwd = os.getcwd()
if og_cwd.split('/')[-1] == 'scripts':
    os.chdir('/'.join(og_cwd.split('/')[:-1]))
    
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

# Deposit temporary script to set up .git
with open('gitploy.py', 'w') as f:
    f.write(gitploy)

# Set up .git
subprocess.check_call([environment + '/bin/python', 'gitploy.py'])

# Remove the temporary script
os.remove('gitploy.py')

