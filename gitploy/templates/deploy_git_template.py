# Bootstrap .git connection with dulwich

import os
from dulwich import porcelain

url = "$url"
cwd = os.getcwd()

assert isinstance(url, str)

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = porcelain.open_repo(cwd)
else:
    print(f"Cloning remote repository from {url} to {cwd}")
    repo = porcelain.clone(url, cwd)