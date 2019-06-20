from auger.cli.cli import cli


class TestModelCLI():
    def test_deploy(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['model', 'deploy'])
        print(result.output)
        print(log.messages)
        assert result.exit_code == 0

    def test_predict(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['model', 'predict'])
        print(result.output)
        print(log.messages)
        assert result.exit_code == 0
