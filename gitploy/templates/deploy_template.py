# Bootstrap a virtual environment (see https://github.com/ybnd/bootstrap-venv)
import os
import sys
from distutils.util import strtobool
import subprocess
from string import Template


url = "$url"
environment = "$environment"
branch = "$branch"
name = "$name"

deploy_git = '''$deploy_git'''
setup_scripts = [
    '''$setup0''',
    '''$setup1''',
    '''$setup2''',
    '''$setup3''',
    '''$setup4''',
    '''$setup5''',
    '''$setup6''',
    '''$setup7''',
    '''$setup8''',
    '''$setup9''',
]

wrap = $wrap
wrapped_template = '''$wrapped_template'''

do = strtobool(
    input(f"Deploy {name} from {url} ({branch}) into {os.getcwd()}? (y/n) \n")
)

if do:
    print(f"Creating a virtual environment in {environment}")
    subprocess.check_call(['python', '-m', 'venv', environment])

    if environment:
        if os.path.isdir(os.path.join(environment, 'bin')):
            executable = os.path.join(environment, 'bin/python')
        elif os.path.isdir(os.path.join(environment, 'Scripts')):
            executable = os.path.join(environment, 'Scripts/python')
        else:
            raise OSError('The virtual environment has an unexpected format.')
    else:
        executable = sys.executable

    # Install gitploy requirements
    subprocess.check_call([executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([executable, '-m', 'pip', 'install', *$install_requirements])

    # Set up .git
    subprocess.check_call([executable, '-c', deploy_git])

    # Install project requirements
    subprocess.check_call([executable, '-m', 'pip', 'install', '-r', '$requirements_file'])

    # Run setup scripts
    for script in setup_scripts:
        if script:
            subprocess.check_call([executable, '-c', script])

    # Write scripts to file
    update = "$update_dir"
    if not os.path.isdir(os.path.dirname(update)):
        os.mkdir(os.path.dirname(update))

    with open(update, 'w+') as f:
        f.write('''$update''')

    # Wrap scripts
    if wrap is not None:
        for file, wrapped in wrap.items():
            with open(wrapped, 'w+') as f:
                f.write(
                    Template(wrapped_template).substitute(
                        file=file, environment=environment,
                    )
                )

    # Remove this script
    os.remove(__file__)

    input('\nDone.')
