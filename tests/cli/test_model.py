from auger.cli.cli import cli


class TestModelCLI():
    def test_deploy(self, log, runner, project, authenticated):
        result = runner.invoke(cli, ['model', 'deploy'])
        print(result.output)
        print(log.messages)
        assert result.exit_code == 0

    def test_predict(self, log, runner, project, authenticated):
        result = runner.invoke(cli, ['model', 'predict', 'iris.csv'])
        print(result.output)
        print(log.messages)
        assert result.exit_code == 0
