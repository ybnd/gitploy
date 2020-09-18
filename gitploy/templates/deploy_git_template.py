# Bootstrap .git connection with GitPython

import os
import glob
import shutil
from git import Repo

url = "$url"
name = "$name"
version = "$version"

cwd = os.getcwd()
temp = f'{name}-{version}-temp'

assert isinstance(url, str)

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = Repo(cwd)
else:
    print(f"Cloning remote repository from {url} to {cwd}/{temp}/")
    repo = Repo.clone_from(url, os.path.join(cwd, temp))

repo.git.checkout(version)

if not os.path.isdir('.git'):
    # Move clone into parent directory (cwd)
    for i in glob.glob(f'{temp}/*') + glob.glob(f'{temp}/.*'):
        shutil.move(i, cwd)

# Remove the (empty) clone directory
shutil.rmtree(temp)
