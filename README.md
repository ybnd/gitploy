# gitploy

## notes:
* This should work more like a CLI utility that spits out a Python script that can then be used to deploy an application in one go
  * Deploys an gitploy-update.py script -- to update the repository
  * Deploys an gitploy-version.py script -- to set the repository to a specific version (by tag or branch)
  * The repository that this deployment script links to should have a .gitploy file that specifies some parameters (e.g. the branch or tag to clone)
  * The repository that this deployment script links to should .gitignore gitploy scripts
