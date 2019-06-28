# Aurer.ai
Auger Cloud python and command line interface


# CLI commands

- auth - allows to login into Auger Cloud
  - login
  - logout
  - whoami

- new - creates local folder for your Project and puts there auger.yaml;
auger.yaml provides local context for the Project and keeps settings for Experiment(s)

- project
  - list - list all Projects for your Organization.
  - select - selects existing Project and stores it's name in auger.yaml;
  all further operations with DataSet(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - create - creates Project on Auger Cloud; Project name will be stored in auger.yaml;
  all further operations with DataSet(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - delete - deletes Project on Auger Cloud and clears Project name from auger.yaml
  - start - starts Project cluster.
  - stop - stops Project cluster.

- dataset
  - list - list all DataSets(s) for the Project.
  - select - selects existing DataSet and stores it's name in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSet.
  - create - creates new DataSet on Auger Cloud from the local or remote data file;
  name of the DataSet will be stored in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSet.
  - delete - deletes DataSet on Auger Cloud and clears DataSet name from auger.yaml

- experiment
  - start - starts Experiment with selected DataSet; Experiment settings configured in auger.yaml
  - stop - stops running experiment.
  - leaderboard - shows leaderboard of the currently running or the last completed experiment.
  - history - shows history (leaderboards and settings) of the previous experiment runs.

- model
  - list - lists all deployed models on Auger Cloud; auger.ai don't keep track of locally deployed models.
  - deploy - deploys selected model locally or on Auger Cloud.
  - predict - predicts using deployed model.


# Auger.ai API
## Base Classes
### auger.api.Context
Context provides environment to run Auger Experiments and Models:
- loads Auger Credentials and initializes Auger REST API to communicate
with remote Auger Cloud;
- loads Auger settings from auger.yaml and provides access to these settings
to Auger classes and business objects;
- provides logging interface to all Auger classes and business objects.

Credentials could be acquired using Auger CLI auth command or loaded from Auger website.
Credentials lookup and loading order:
- form environment variable AUGER_CREDENTIALS set with content of
  the credentials json;
- from auger.json file, path to folder with credentials set with
  environment variable AUGER_CREDENTIALS_PATH;
- from auger.json file, path to folder with credentials set with
  path_to_credentials key in auger.yaml
- if none above, form $HOME/.augerai/auger.json

### auger.api.Project
Project provides interface to Auger Project.

- **Project(context, project_name)** - constructs Project instance.
  - context - instance of auger.api.Context.
  - project_name - name of the existing or new Project, optional.

- **list()** - lists all Projects in your Organization. Returns iterator where
  each item is dictionary with Project properties. Throws exception if can't
    validate credentials or network connection error.

  Example:
  ```
  ctx = Context()
  for project in iter(Project(ctx).list()):
    ctx.log(project.get('name'))
  ```

- **create()** - creates Project on Auger Cloud. Throws exception if can't
  validate credentials, Project with such name already exists, or network
  connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, new_project_name).create()
  ```

- **delete()** - deletes Project on Auger Cloud. Throws exception if can't
  validate credentials, Project with such name doesn't exist, or network
  connection error.

  Example:
  ```
  ctx = Context()
  Project(ctx, existing_project_name).delete()
  ```

- **start()** - starts Project cluster. DataSet processing, Experiment runs
  and Model deploy and predict need cluster to perform operations and will
  start cluster automatically. It is possible, but not necessary, to start
  cluster beforehand. Throws exception if can't validate credentials or
  network connection error.

  Project cluster configuration defined in auger.yaml:
  ```
  cluster:
    # Cluster node type: standard|high_memory
    type: high_memory
    # Minimal number of cluster nodes
    min_nodes: 2
    # Maximum number of cluster nodes
    max_nodes: 4
    # Cluster software stack version - optional
    stack_version: experimental
  ```

  Example:
  ```
  ctx = Context()
  Project(ctx, project_name).start()
  ```

- **stop()** - stops Project cluster. DataSet processing, Experiment runs
  and Model deploy and predict need cluster to perform operations and will
  start cluster automatically. Cluster will stop automatically after some
  inactivity period. To stop it explicitly, use Project stop() method.
  Throws exception if can't validate credentials, such project doesn't exist,
  or network connection error.

  Example:
  ```
  ctx = Context()
  Project(ctx, project_name).stop()
  ```

- **properties()** - returns dictionary with Project properties. Throws exception
  if can't validate credentials, such Project doesn't exist, or network connection
  error.

  Example:
  ```
  ctx = Context()
  properties = Project(ctx, project_name).properties()
  ```


### auger.api.DataSet
DataSet for training on Auger Cloud.

- **DataSet(context, project, dataset_name)** - constructs DataSet instance.
  - context - instance of auger.api.Context.
  - project - instance of auger.api.Project pointing to existing remote project.
  - dataset_name - name of the existing or new DataSet, optional.

- **list()** - lists all DataSets(s) for the Project. Returns iterator where
  each item is dictionary with DataSet properties. Throws exception if can't
  validate credentials, parent project doesn't exist, or network connection error.


  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  for dataset in iter(DataSet(ctx, project).list()):
      ctx.log(dataset.get('name'))
  ```

- **create(source)** - creates new DataSet on Auger Cloud from the local or
  remote data file. If `dataset_name` is not set, name will be selected
  automatically. Throws exception if can't validate credentials, parent project
  doesn't exist, DataSet with specified name already exists, or network
  connection error.

  - source - path to local or link to remote .csv or .arff file

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project).create('../iris.csv')
  ctx.log('Created dataset %s' % dataset.name)
  ```

- **delete()** - deletes DataSet on Auger Cloud. Throws exception if can't
  validate credentials, parent project doesn't exist, DataSet with specified
  name doesn't exist, or network connection error.       

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  DataSet(ctx, project, dataset_name).delete()
  ctx.log('Deleted dataset %s' % dataset_name)
  ```

- **properties()** - returns dictionary with DataSet properties. Throws exception
  if can't validate credentials, such DataSet doesn't exist, or network connection
  error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  properties = DataSet(ctx, dataset_name).properties()
  ```


### auger.api.Experiment
### auger.api.Model


## Development Setup

We strongly recommend to install Python virtual environment:

```
$ pip install virtualenv virtualenvwrapper
```

Clone Auger Cloud repo:

```
$ git clone https://github.com/deeplearninc/auger-ai
```

Setup dependencies and Auger command line:

```
$ pip install -e .[all]
```

Running tests and getting test coverage:

```
$ pytest --cov='auger' --cov-report html tests/
```

#
