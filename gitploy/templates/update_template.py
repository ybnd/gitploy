# Update repository ~ git pull

import os
import subprocess

def find_env(cd = os.getcwd()):
    if os.path.isdir(os.path.join(cd, '$environment')):
        return cd
    else:
        return find_repo(os.path.dirname(cd))

update = """
import os
from git import Repo, GitCommandError

def find_repo(cd = os.getcwd()):
    if os.path.isdir(os.path.join(cd, '.git')):
        return cd
    else:
        return find_repo(os.path.dirname(cd))

repo = Repo(find_repo())
try:
    repo.git.checkout('$branch')
    repo.git.pull()
except GitCommandError:
    print('Could not update.')
"""

# Get location of executable in environment
if os.name == 'nt':
    # On Windows
    executable = os.path.join(find_env(), '$environment/Scripts/python')
else:
    # On Linux
    executable = os.path.join(find_env(), '$environment/bin/python')

subprocess.check_call([executable, '-c', update])
