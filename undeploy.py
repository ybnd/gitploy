import os
import shutil

if os.path.isfile('README.md'):
    os.remove('README.md')

if os.path.isdir('.git')
    shutil.rmtree('.git')