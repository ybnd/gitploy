# gitploy

Generate short scripts to deploy functional Python development environments without the hassle.

* Runs an optional check script
* Bootstraps a virtual environment
* Clones your project with [GitPython](https://gitpython.readthedocs.io/en/stable/)
* Installs your project’s dependencies in the new virtual environment
* Runs some optional setup scripts

### Use case

I use `gitploy` to deploy experimental code to a few users that don’t necessarily want to figure things out. This library allows me to keep the users’ environments clean and as close as possible to my own development environment. This makes for easy debugging and iteration.

I would not advise using it in any other case. 

### Installation

```shell
git clone https://github.com/ybnd/gitploy
cd gitploy
pip install -e .
```

### Usage

1. Write a `.ploy` file for your release (get it? you’ve now got `.git` and `.ploy` haha)

    ```yaml
    name: <your project>
    version: <the version to deploy>
    url: <the url of your repo>
    
    environment: <the name of the virtual environment, defaults to '.venv'>				
    check: <path to check script templates>
    setup: 
        - <paths to setup script templates>
        - ...
    ```

2. Write some script templates, in a way that [string.Template](https://docs.python.org/3/library/string.html?highlight=template#string.Template) can understand, i.e. the placeholder for `name` in your `.ploy` file should be `$name`.

   The check script is run *before* the virtual environment is created, so it shouldn’t refer to `$environment`  and should not require anything but the standard libraries.

   All of these should be checked into your project’s version control, as `gitploy` doesn’t bundle them into the deployment script.

3. Run `gitploy` in your project directory:

    ```shell
    python -m gitploy
    ```

    will generate a deployment script at `deploy_$name-$version.py`. 

### Used for

* https://github.com/ybnd/isimple