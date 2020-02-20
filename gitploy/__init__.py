import yaml
import yaml.representer
from string import Template

from gitploy.templates import *

# https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
yaml.add_representer(
    dict,
    lambda self, data: yaml.representer.SafeRepresenter.represent_dict(
        self, data.items()
    )
)


DEFAULT = {
    'url': '',
    'name': '',
    'environment': '.venv',
    'requirements': ['dulwich'],
    'templates': {
        'update': 'templates/update_template.py',
        'version': 'templates/version_template.py',
    },
}


if __name__ == '__main__':
    if os.path.isfile('.gitploy'):
        with open('.gitploy', 'r') as f:
            config = yaml.safe_load(f.read())
    else:
        config = {}

    for key in DEFAULT.keys():
        if key not in config:
            config[key] = DEFAULT[key]

    update = Template(update).substitute(
        url=config['url'],
    )

    version = Template(version).substitute(
        url=config['url'],
    )

    deploy_git = Template(deploy_git).substitute(
        url=config['url'],
    )

    deploy = Template(deploy).substitute(
        environment=config['environment'],
        requirements=str(config['requirements']),
        deploy_git=deploy_git,
        update_dir=config['templates']['update'],
        update=update,
        version_dir=config['templates']['version'],
        version=version,
    )

    fname = f"deploy_{config['name']}.py"
    if os.path.isfile(fname):
        os.remove(fname)

    with open(fname, 'w') as f:
        f.write(deploy)
