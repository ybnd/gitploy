import os
from dulwich import porcelain

cwd = os.getcwd()
url = "https://github.com/ybnd/gitploy"
branch = 'master'

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = porcelain.open_repo(cwd)
else:
    print(f"Cloning remote repository from {url} to {cwd}")
    repo = porcelain.clone(url ,cwd)

fetched_data = porcelain.fetch(repo, url)