import os
from dulwich import porcelain
import yaml


cwd = os.getcwd()

if os.path.isfile('.ploy'):
    with open('.ploy', 'r') as f:
        ploy = yaml.safe_load(f.read())

if os.path.isdir('.git'):
    print(f"Opening repository in {cwd}")
    repo = porcelain.open_repo(cwd)
else:
    print(f"Cloning remote repository from {ploy['url']} to {cwd}")
    repo = porcelain.clone(ploy['url'] ,cwd)

fetched_data = porcelain.fetch(repo, ploy['url'])