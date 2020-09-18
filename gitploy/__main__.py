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
    'environment': '',
    'install_requirements': ['GitPython'],
    'requirements_file': 'requirements.txt',
    'setup': [],
    'destinations': {
        'update': 'scripts/update.py',
    },
    'wrap': None,
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
        environment=config['environment'],
        branch=config['branch'],
        name=config['name'],
    )

    deploy_git = Template(deploy_git).substitute(
        url=config['url'],
        branch=config['branch'],
        name=config['name'],
    )

    setup = []

    if config['setup'] is not None:
        if len(config['setup']) > 10:
            raise ValueError("Can't support more than 10 setup scripts")   
        for script in config['setup']:
            with open(script, 'r') as f:
                setup.append(
                    Template(f.read()).substitute(
                        environment=config['environment'],
                    )
                )
                
    setup += [''] * (10 - len(setup))

    deploy = Template(deploy).substitute(
        url=config['url'],
        environment=config['environment'],
        name=config['name'],
        branch=config['branch'],
        install_requirements=str(config['install_requirements']),
        requirements_file=config['requirements_file'],
        deploy_git=deploy_git,
        **{f"setup{i}":script for i, script in enumerate(setup)},
        update_dir=config['destinations']['update'],
        update=update,
        wrap=config['wrap'],  # todo: make sure that wrap is Dict[str,str]
        wrapped_template=wrapped,
    )

    fname = f"deploy_{config['name']}.py"
    if os.path.isfile(fname):
        os.remove(fname)

    with open(fname, 'w') as f:
        f.write(deploy)
