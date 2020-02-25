# Bootstrap .git connection with GitPython

import os
from git import Repo

url = "$url"
branch = "$branch"

cwd = os.getcwd()

assert isinstance(url, str)

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = Repo(cwd)
else:
    print(f"Cloning remote repository from {url} to {cwd}")
    repo = Repo.clone_from(url, os.path.join(cwd, "$name"))

repo.git.checkout(branch)
