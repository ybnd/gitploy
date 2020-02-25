# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)
import os
import shutil
import subprocess


# Remove this script (directory must be empty!)
os.remove(__file__)

environment = "$environment"
name = "$name"

deploy_git = '''$deploy_git'''
setup = '''$setup'''

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
subprocess.check_call([executable, '-m', 'pip', 'install', '-r', '$name/$requirements_file'])

if setup:
    subprocess.check_call([executable, '-c', setup])

# Write scripts to file
update = os.path.join(name, "$update_dir")
if not os.path.isdir(os.path.dirname(update)):
    os.mkdir(os.path.dirname(update))

with open(update, 'w+') as f:
    f.write('''$update''')

# Move virtual environment into the repository directory
shutil.move(environment, name)
