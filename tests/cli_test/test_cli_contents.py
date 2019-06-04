from click.testing import CliRunner

from auger.cli.cli import cli

from .constants import COMMAND_STRUCTURE


class TestCliTableOfContents(object):

    def test_bare_call(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'auth' in result.output
        assert 'clusters' in result.output
        assert 'cluster_tasks' in result.output
        assert 'help' in result.output
        assert 'instance_types' in result.output
        assert 'orgs' in result.output
        assert 'projects' in result.output
        assert 'experiments' in result.output
        assert 'experiment_sessions' in result.output
        assert 'pipelines' in result.output
        assert 'trials' in result.output
        assert 'cluster_status' in result.output

    def test_sections_contents(self):
        runner = CliRunner()
        for command, subcommands in COMMAND_STRUCTURE.items():
            # 2) check subcommands
            if subcommands is not None:
                for subcommand in subcommands:
                    result = runner.invoke(cli, [command, subcommand])
                    assert result.exit_code == 0
            else:
                # 1) check command itself
                result = runner.invoke(cli, [command, '--help'])
                assert result.exit_code == 0

