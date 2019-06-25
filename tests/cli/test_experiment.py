import os

from auger.cli.cli import cli
from auger.api.utils.config_yaml import ConfigYaml
from .utils import interceptor, ORGANIZATIONS, PROJECTS


PROJECT_FILES = {}
EXPERIMENTS = {}

class TestExperimentCLI():
    def test_list(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': {
                'meta': {
                    'status': 200,
                    'pagination': {
                        'count': 2, 'offset': 0, 'total': 2, 'limit': 100}
                },
                'data': [
                {'id': 1, 'name': 'test_dataset1'},
                {'id': 2, 'name': 'test_dataset2'}
                ],
            },
            'get_experiments': {
                'meta': {
                    'pagination': {
                        'total': 0, 'offset': 0, 'limit': 100, 'count': 0},
                     'status': 200},
                'data': [{}, {}]}
        }
        interceptor(PAYLOAD, monkeypatch)
        runner.invoke(cli, ['dataset', 'create', 'iris.csv'])
        # print(os.listdir())
        # config = ConfigYaml()
        # config.load_from_file('auger.yaml')
        # config.yaml.dataset = 'iris-1.csv'
        # config.write('auger.yaml')
        # with open('auger.yaml', 'r') as f:
        #     print(f.read())
        result = runner.invoke(cli, ['experiment', 'list'])
        assert result.exit_code == 0
        assert log.messages[-1] == '2 Experiment(s) listed'

    def test_start(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': {},
            'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code == 0

    def test_start_without_target(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': {},
            'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        # TODO: ensure cli throws error on trying to start exp w/o target
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code != 0
        assert log.messages[-1] == 'Please set target to build model.'

    def test_status(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': {},
            'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'status'])
        assert result.exit_code == 0

    def test_stop(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': {},
            'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'stop'])
        assert result.exit_code == 0

    def test_leaderboard(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project': {},
            'get_project_files': PROJECT_FILES,
            # 'get_experiments': EXPERIMENTS,
            # 'get_experiment_sessions': {},
            # 'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        runner.invoke(cli, ['dataset', 'create', 'iris.csv'])
        result = runner.invoke(cli, ['experiment', 'leaderboard'])
        print(result.output, log.messages)
        assert result.exit_code == 0

    def test_history(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': {},
            'get_trials': {},
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'history'])
        assert result.exit_code == 0
