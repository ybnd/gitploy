import os

templates = os.path.dirname(__file__)

with open(os.path.join(templates, 'deploy_template.py'), 'r') as f:
    deploy = f.read()

with open(os.path.join(templates, 'deploy_git_template.py'), 'r') as f:
    deploy_git = f.read()

with open(os.path.join(templates, 'update_template.py'), 'r') as f:
    update = f.read()

with open(os.path.join(templates, 'version_template.py'), 'r') as f:
    version = f.read()

with open(os.path.join(templates, 'wrapped_template.py'), 'r') as f:
    wrapped = f.read()