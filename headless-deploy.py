# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)
import os
import re
import subprocess


environment = '.venv'
requirements = ['dulwich']


gitploy = '''# Bootstrap .git connection with dulwich

import os
from dulwich import porcelain

url = 'https://github.com/ybnd/gitploy'
cwd = os.getcwd()

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = porcelain.open_repo(cwd)
else:
    print(f"Cloning remote repository from {url} to {cwd}")
    repo = porcelain.clone(url, cwd)

fetched_data = porcelain.fetch(repo, url)
'''


# Create a virtual environment in .venv
subprocess.check_call(['python', '-m', 'venv', environment])

# Install requirements.txt
subprocess.check_call([environment + '/bin/python', '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([environment + '/bin/python', '-m', 'pip', 'install', *requirements])

# Deposit temporary script to set up .git
with open('gitploy.py', 'w') as f:
    f.write(gitploy)

# Set up .git
subprocess.check_call([environment + '/bin/python', 'gitploy.py'])

# Remove the temporary script
os.remove('gitploy.py')

# Remove this script
os.remove(__file__)

