# Run $file with the virtual environment in $environment

import os
import subprocess

if __name__ == '__main__':
    environment = '$environment'

    if os.path.isdir(os.path.join(environment, 'bin')):
        os.environ['PATH'] += os.pathsep + os.path.join(os.getcwd(), '.venv/bin')
        executable = os.path.join(environment, 'bin/python')
    elif os.path.isdir(os.path.join(environment, 'Scripts')):
        os.environ['PATH'] += os.pathsep + os.path.join(os.getcwd(), '.venv/Scripts')
        executable = os.path.join(environment, 'Scripts/python')
    else:
        raise OSError('The virtual environment has an unexpected format.')

    subprocess.call([executable, '$file'])
