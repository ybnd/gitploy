import os

templates = os.path.dirname(__file__)

with open(os.path.join(templates, 'deploy_template.py'), 'r') as f:
    deploy = f.read()

with open(os.path.join(templates, 'deploy_git_template.py'), 'r') as f:
    deploy_git = f.read()
