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
    'branch': 'master',
    'name': '',
    'environment': '.venv',
    'install_requirements': ['GitPython'],
    'requirements_file': 'requirements.txt',
    'setup': None,
    'destinations': {
        'update': 'scripts/update.py',
    },
}


if __name__ == '__main__':
    if os.path.isfile('.ploy'):
        with open('.ploy', 'r') as f:
            config = yaml.safe_load(f.read())
    else:
        config = {}

    for key in DEFAULT.keys():
        if key not in config:
            config[key] = DEFAULT[key]

    config['install_requirements'] = list(
        set(DEFAULT['install_requirements'] + config['install_requirements'])
    )

    update = Template(update).substitute(
        branch=config['branch'],
        name=config['name'],
    )

    deploy_git = Template(deploy_git).substitute(
        url=config['url'],
        branch=config['branch'],
        name=config['name'],
    )

    if config['setup'] is not None:
        with open(config['setup'], 'r') as f:
            setup = f.read()

        setup = Template(setup).substitute(
            environment=config['environment'],
        )
    else:
        setup = ''

    deploy = Template(deploy).substitute(
        environment=config['environment'],
        name=config['name'],
        install_requirements=str(config['install_requirements']),
        requirements_file=config['requirements_file'],
        deploy_git=deploy_git,
        setup=setup,
        update_dir=config['destinations']['update'],
        update=update,
    )

    fname = f"deploy_{config['name']}.py"
    if os.path.isfile(fname):
        os.remove(fname)

    with open(fname, 'w') as f:
        f.write(deploy)
