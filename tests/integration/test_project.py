import pytest
from auger.cli.cli import cli


class TestProjectCLI ():
    def test_create_list_delete(self, runner, log, project):
        result = runner.invoke(cli, ['project', 'delete', 'cli-integration-test'])

        result = runner.invoke(cli, ['project', 'create', 'cli-integration-test'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Created Project cli-integration-test'

        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0
        assert 'cli-integration-test' in str(log.messages)

        result = runner.invoke(cli, ['project', 'delete', 'cli-integration-test'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Deleted Project cli-integration-test'

    def test_start_stop(self, runner, log, project):
        result = runner.invoke(cli, ['project', 'delete', 'cli-integration-test'])

        result = runner.invoke(cli, ['project', 'create', 'cli-integration-test'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Created Project cli-integration-test'

        result = runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0
        assert log.messages[-5] == 'Starting Project...'
        assert log.messages[-4] == 'Project status is deploying...'
        assert log.messages[-3] == 'Project status is deployed...'
        assert log.messages[-2] == 'Project status is running...'
        assert log.messages[-1] == 'Started Project cli-integration-test'

        result = runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0
        assert log.messages[-4] == 'Stopping Project...'
        assert log.messages[-3] == 'Project status is undeploying...'
        assert log.messages[-2] == 'Project status is undeployed...'
        assert log.messages[-1] == 'Stopped Project cli-integration-test'

        result = runner.invoke(cli, ['project', 'delete', 'cli-integration-test'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Deleted Project cli-integration-test'
