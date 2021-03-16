# Deployment file generated by gitploy $gitploy https://github.com/ybnd/gitploy

# To deploy, place the file into an empty folder and run it.
#          (on Windows, it's enough to just double-click it)

# Bootstraps a virtual environment in
environment = "$environment"
# ...or doesn't, if it says environment = ""

# Sets up a git repository for
name = "$name"
url = "$url"
version = "$version"

# Installs its dependencies in the virtual environment
# Runs the following script templates for $name:
setup_script_templates = $setup
# You can read them here: $url/tree/$version/scripts

# Progress is logged to
LOG = ".deploy.log"
# If the deployment succeeds, this file will be renamed to
SUCCESS = ".success.log"
# If the deployment fails, it will be renamed to
FAILURE = "failure.log"

# The result is a fully functional development environment without the hassle.


import os
import sys
import glob
import time
import shutil
import logging
import threading
from distutils.util import strtobool
from contextlib import contextmanager
from itertools import cycle
import subprocess
from string import Template

install_requirements = $install_requirements
requirements_file = "$requirements_file"

check = '''$check'''
deploy_git = '''$deploy_git'''

# Remove previous log files:
for log in glob.glob("*.log"):
    os.remove(log)

@contextmanager
def waiton(message):
    stdout = sys.stdout
    stop = threading.Event()
    ok = True

    def _animation():
        for frame in cycle("-\\|/"):
            if stop.is_set():
                break
            stdout.write("\r"+ frame + " " + message + " ")
            stdout.flush()
            time.sleep(0.15)

    try:
        log.debug(message)
        threading.Thread(target=_animation).start()
        yield
    except Exception as e:
        ok = False
        raise e
    finally:
        stop.set()
        if ok:
            stdout.writelines([
                "\r+ Done " + message[0].lower() + message[1:] + "\n"
            ])
        else:
            stdout.write("\r- " + message + "\n")



def run(*args):
    stdout = sys.stdout

    with open(LOG, "a+") as f:
        sys.stdout = f
        try:
            subprocess.check_call(args, stdout=f, stderr=f)
        finally:
            sys.stdout = stdout


def hang(code = 0):
    input("<press any key to exit> ")
    exit(code)


def cancel():
    log.info("Canceled.")
    hang()


def log_script(script):
    log.debug(f"\n{'=' * 80}\n{script}\n{'=' * 80}\n")


log = logging.getLogger()
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter("%(message)s"))
log.addHandler(sh)
fh = logging.FileHandler(LOG)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
log.addHandler(fh)


do = input(f"Deploy {name} from {url} ({version}) into {os.getcwd()}? (y/N) ")

if do == '' or not strtobool(do):
    cancel()

if os.path.exists(environment):
    overwrite = input(
        f"Overwrite virtual environment {os.getcwd()}/{environment}? (Y/n) "
    )
    if overwrite == '' or strtobool(overwrite):
        shutil.rmtree(environment)
    else:
        cancel()


if os.path.exists(".git"):
    overwrite = input(
        f"Overwrite git repository in {os.getcwd()}/.git? (Y/n) "
    )
    if overwrite == '' or strtobool(overwrite):
        shutil.rmtree(".git")
    else:
        cancel()


try:
    if check:
        with waiton("Running check script"):
            log_script(check)
            run('python', '-c', check)

    with waiton(f"Creating virtual environment in {environment}"):
        run('python', '-m', 'venv', environment)

    if os.path.isdir(os.path.join(environment, 'bin')):
        executable = os.path.join(environment, 'bin/python')
    elif os.path.isdir(os.path.join(environment, 'Scripts')):
        executable = os.path.join(environment, 'Scripts/python')
    else:
        raise OSError(
            'The virtual environment has an unexpected format.'
        )

    with waiton("Installing gitploy requirements"):
        pip_install = [executable, '-m', 'pip', 'install']
        run(*pip_install, '--upgrade', 'pip')
        run(*pip_install, *install_requirements)

    with waiton("Deploying git repository"):
        log_script(deploy_git)
        run(executable, '-c', deploy_git)

    with waiton("Installing project requirements"):
        run(*pip_install, '-r', requirements_file)

    with waiton("Running setup scripts"):
        for script_template in setup_script_templates:
            with open(script_template, 'r') as f:
                script = Template(f.read()).substitute(
                    name=name,
                    url=url,
                    version=version,
                    environment=environment
                )
                log_script(script)
                run(executable, '-c', script)

    # Remove this script
    os.remove(__file__)
    logging.shutdown()
    os.rename(LOG, SUCCESS)
    hang()
except subprocess.CalledProcessError as e:
    log.info(f"Failed to deploy!")
    logging.shutdown()
    os.rename(LOG, FAILURE)
    hang(1)
