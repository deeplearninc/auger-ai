import os

from auger.cli.cli import cli
from auger.api.utils.config import Config


class TestNewCommand():

    def test_minimal_arguments_successfull_creation(self, runner, isolated):
        # successful status
        result = runner.invoke(cli, ['new', 'test_project'])
        assert result.exit_code == 0

        # directory created
        target_dir = os.path.join(os.getcwd(), 'test_project')
        assert os.path.exists(target_dir) and os.path.isdir(target_dir)

        # config file exists
        config_file = os.path.join(target_dir, 'auger.yaml')
        assert os.path.exists(config_file)

        # config contains proper data
        config = Config().load('test_project')
        assert config.get('name', '') == 'test_project'

    def test_project_with_given_name_already_exists(
            self, runner, log, project):
        os.chdir('..')
        runner.invoke(cli, ['new', 'test_project'])
        result = runner.invoke(cli, ['new', 'test_project'])
        assert result.exit_code != 0
        assert (log.records[-1].message ==
                "Can't create 'test_project'. Folder already exists.")

    def test_nested_project_forbidden(self, runner, log, project):
        result = runner.invoke(cli, ['new', 'test_project'])
        assert result.exit_code != 0
        assert (log.records[-1].message ==
                "Can't create 'test_project' inside a project."
                " './auger.yaml' already exists")

    def test_full_set_of_arguments(self, log, runner, isolated, project):
        os.chdir('..')
        result = runner.invoke(
            cli, [
                'new', 'new_project',
                '--model-type', 'regression',
                '--target', 'target_column',
                '--source', 'test_project/iris.csv'])

        assert result.exit_code == 0
        config = Config().load('new_project')
        assert config.get('model_type', '') == 'regression'
        assert config.get('target', '') == 'target_column'
        assert config.get('source', '') == os.path.join(
            os.getcwd(), 'test_project', 'iris.csv')

    def test_bad_source(self, log, runner, isolated):
        result = runner.invoke(
            cli, ['new', 'test_project', '--source', 'not_existing_file.csv'])
        assert result.exit_code != 0
        assert log.messages[-1].startswith("Can't find file to import:")

    def test_source_wrong_extension(self, log, runner, isolated):
        result = runner.invoke(
            cli, ['new', 'test_project', '--source', 'file_with_wrong.extension'])
        assert result.exit_code != 0
        assert log.messages[-1] ==\
             'Source file has to be one of the supported fomats: .csv, .arff'
