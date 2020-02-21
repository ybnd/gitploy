# Update repository ~ git pull
import os
import subprocess
from dulwich import porcelain
from distutils.util import strtobool


def find_repo(cd = os.getcwd()):
    if os.path.isdir(os.path.join(cd, '.git')):
        return cd
    else:
        return find_repo(os.path.dirname(cd))


if __name__ == '__main__':
    repo = porcelain.open_repo(find_repo())
    porcelain.pull(repo, '$url')
