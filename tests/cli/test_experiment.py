from auger.cli.cli import cli


class TestExperimentCLI():
    def test_list(self, runner, isolated, monkeypatch):
        monkeypatch.setattr(RestApi, 'call_ex', experiment_list)
        result = runner.invoke(cli, ['experiment', 'list'])
        assert result.exit_code == 0

    def test_start(self, runner, isolated):
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code == 0

    def test_start_without_target(self, log, runner, isolated):
        # TODO: ensure cli trows error on try to start exp w/o target
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code != 0
        assert log.messages[-1] == 'Please set target to build model.'

    def test_status(self, runner, isolated):
        result = runner.invoke(cli, ['experiment', 'status'])
        assert result.exit_code == 0

    def test_stop(self, runner, isolated):
        result = runner.invoke(cli, ['experiment', 'stop'])
        assert result.exit_code == 0

    def test_leaderboard(self, runner, isolated):
        result = runner.invoke(cli, ['experiment', 'leaderboard'])
        assert result.exit_code == 0

    def test_history(self, runner, isolated):
        result = runner.invoke(cli, ['experiment', 'history'])
        assert result.exit_code == 0
