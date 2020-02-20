# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)
import os
import subprocess

environment = '$environment'
requirements = '$requirements'
deploy_git = '''$deploy_git'''

# Create a virtual environment in .venv
subprocess.check_call(['python', '-m', 'venv', environment])

if os.path.isdir(os.path.join(environment, 'bin')):
    executable = os.path.join(environment, 'bin/python')
elif os.path.isdir(os.path.join(environment, 'Scripts')):
    executable = os.path.join(environment, 'Scripts/python')
else:
    raise OSError('The virtual environment has an unexpected format.')

# Install requirements
subprocess.check_call([executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([executable, '-m', 'pip', 'install', *requirements])

# Set up .git
subprocess.check_call([executable, '-c', deploy_git])

# Write templates to file
with open('$update_dir', 'w+') as f:
    f.write('''$update''')

with open('$version_dir', 'w+') as f:
    f.write('''$version''')

# Remove this script
os.remove(__file__)