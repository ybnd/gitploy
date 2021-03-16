import yaml
import yaml.representer
from subprocess import check_call
from string import Template

from gitploy.templates import *

__version__ = 0.5

# https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
yaml.add_representer(
    dict,
    lambda self, data: yaml.representer.SafeRepresenter.represent_dict(
        self, data.items()
    )
)

DEFAULT = {
    'url': '',
    'version': '',
    'name': '',
    'environment': '',
    'install_requirements': ['GitPython'],
    'requirements_file': 'requirements.txt',
    'check': '',
    'setup': [],                                    # List of setup scripts (relative paths). Will not be packaged in the deploy script, so these should be in the repository
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

    for key in ['url', 'version', 'name', 'environment']:
        if config[key] is None:
            raise ValueError(f'No {key} provided!')

    if config['check']:
        with open(config['check']) as f:
            check = Template(f.read()).substitute(  # limited config
                url=config['url'],
                name=config['name'],
                version=config['version']
            )

            # Run the check when generating deploy script
            check_call(['python', '-c', check])
    else:
        check = config['check']


    config['install_requirements'] = list(
        set(DEFAULT['install_requirements'] + config['install_requirements'])
    )

    deploy_git = Template(deploy_git).substitute(  # limited config
        url=config['url'],
        name=config['name'],
        version=config['version']
    )

    setup = []

    for script in config['setup']:
        setup.append(script)

    deploy = Template(deploy).substitute(
        url=config['url'],
        environment=config['environment'],
        name=config['name'],
        version=config['version'],
        check=check,
        install_requirements=str(config['install_requirements']),
        requirements_file=config['requirements_file'],
        deploy_git=deploy_git,
        setup=setup,
        gitploy=__version__,
    )

    fname = f"deploy_{config['name']}-{config['version']}.py"
    if os.path.isfile(fname):
        os.remove(fname)

    with open(fname, 'w') as f:
        f.write(deploy)
