# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)
import os
import shutil
import subprocess

environment = "$environment"
deploy_git = '''$deploy_git'''
setup = '''$setup'''

# Remove the previous environment or .git folder
if os.path.isdir(environment):
    print(f"Removing previous virtual environment {environment}")
    shutil.rmtree(environment)

if os.path.isdir('.git'):
    print(f"Removing previous .git folder")
    shutil.rmtree('.git')

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
subprocess.check_call([executable, '-m', 'pip', 'install', *$install_requirements])

# Set up .git
subprocess.check_call([executable, '-c', deploy_git])

# Install requirements
subprocess.check_call([executable, '-m', 'pip', 'install', '-r', '$requirements_file'])

if setup:
    subprocess.check_call([executable, '-c', setup])

# Write scripts to file
update = "$update_dir"
if not os.path.isdir(os.path.dirname(update)):
    os.mkdir(os.path.dirname(update))

with open(update, 'w+') as f:
    f.write('''$update''')

version = "$version_dir"
if not os.path.isdir(os.path.dirname(version)):
    os.mkdir(os.path.dirname(version))

with open(version, 'w+') as f:
    f.write('''$version''')

# Remove this script
os.remove(__file__)
