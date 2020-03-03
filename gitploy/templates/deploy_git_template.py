# Bootstrap .git connection with GitPython

import os
import glob
import shutil
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

# Move clone into parent directory (cwd)
for i in glob.glob('$name/*') + glob.glob('$name/.*'):
    shutil.move(i, cwd)

# Remove the (empty) clone directory
shutil.rmtree('$name')
