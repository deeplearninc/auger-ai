import os
import logging

from click.testing import CliRunner

from auger.cli.cli import cli
from auger.cli.utils.config_yaml import ConfigYaml


class TestNewCommand(object):

    def test_minimal_arguments_successfull_creation(self):
        # successful status
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['new', 'test_project'])
            assert result.exit_code == 0

            # directory created
            target_dir = os.path.join(os.getcwd(), 'test_project')
            assert os.path.exists(target_dir) and os.path.isdir(target_dir)

            # config file exists
            config_file = os.path.join(target_dir, 'auger.yaml')
            assert os.path.exists(config_file)

            # config contains proper data
            config = ConfigYaml()
            config.load_from_file(config_file)
            assert config.project == 'test_project'

    def test_project_with_given_name_already_exists(self, caplog):
        caplog.set_level(logging.INFO)
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ['new', 'test_project'])
            result = runner.invoke(cli, ['new', 'test_project'])
            assert result.exit_code != 0
            assert (caplog.records[-1].message ==
                    "Can't create 'test_project'. Folder already exists.")

    def test_nested_project_forbidden(self, caplog):
        caplog.set_level(logging.INFO)
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ['new', 'test_project'])
            os.chdir('test_project')
            result = runner.invoke(cli, ['new', 'test_project'])
            assert result.exit_code != 0
            assert (caplog.records[-1].message ==
                    "Can't create 'test_project' inside a project."
                    " './auger.yaml' already exists")

    def test_dataset(self):
        # TODO: dataset cration fact
        # TODO: dataset parameters setting
        assert False

    def test_full_set_of_arguments(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli, [
                    'new', 'test_project',
                    '--model-type', 'regression',
                    '--target', 'target_column'])
            assert result.exit_code == 0
            config_path = os.path.join(
                os.getcwd(), 'test_project', 'auger.yaml')
            config = ConfigYaml()
            config.load_from_file(config_path)
            assert config.experiment.type == 'regression'
            assert config.experiment.target == 'target_column'
