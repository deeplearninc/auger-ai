from auger.cli.cli import cli


class TestModelCLI():
    def test_deploy(self, runner, isolated):
        result = runner.invoke(cli, ['model', 'deploy'])
        assert result.exit_code == 0


    def test_predict(self, runner, isolated):
        result = runner.invoke(cli, ['model', 'predict'])
        assert result.exit_code == 0

