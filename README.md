#Aurer.ai
Auger Cloud python and command line interface

#CLI commands

- auth - allows to login into Auger Cloud
  - login
  - logout
  - whoami

- new - creates local folder for your Project and puts there auger.yaml;
auger.yaml provides local context for the Project and keeps settings for Experiment(s)

- project
  - list - list all Projects for your Organization.
  - select - selects existing Project and stores it's name in auger.yaml;
  all further operations with DataSource(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - create - creates Project on Auger Cloud; Project name will be stored in auger.yaml;
  all further operations with DataSource(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - delete - deletes Project on Auger Cloud and clears Project name from auger.yaml

- datasource
  - list - list all DataSource(s) for the Project.
  - select - selects existing DataSource and stores it's name in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSource.
  - create - creates new DataSource on Auger Cloud from the local or remote data file;
  name of the DataSource will be stored in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSource.
  - delete - deletes DataSource on Auger Cloud and clears DataSource name from auger.yaml

- experiment
  - start - starts Experiment with selected DataSource; Experiment settings configured in auger.yaml
  - stop - stops running experiment.
  - leaderboard - shows leaderboard of the currently running or the last completed experiment.
  - history - shows history (leaderboards and settings) of the previous experiment runs.

- model
  - list - lists all deployed models on Auger Cloud; auger.ai don't keep track of locally deployed models.
  - deploy - deploys selected model locally or on Auger Cloud.
  - predict - predicts using deployed model.

#Auger.ai API
## Base Classes
  - Project
  - DataSource
  - Experiment
  - Model


## Development Setup

We strongly recommend to install Python virtual environment:

```
$ pip install virtualenv virtualenvwrapper
```

Clone A2ML:

```
$ git clone https://github.com/deeplearninc/auger-ai
```

Setup dependencies and A2ML command line:

```
$ pip install -e .[all]
```

Running tests and getting test coverage:

```
$ pytest --cov='a2ml' --cov-report html tests/  
```

#
