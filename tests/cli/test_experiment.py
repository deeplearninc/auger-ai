from auger.cli.cli import cli


class TestExperimentCLI():
    def test_list(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'list'])
        assert result.exit_code == 0


    def test_start(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code == 0


    def test_status(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'status'])
        assert result.exit_code == 0


    def test_stop(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'stop'])
        assert result.exit_code == 0


    def test_leaderboard(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'leaderboard'])
        assert result.exit_code == 0


    def test_history(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['experiment', 'history'])
        assert result.exit_code == 0

