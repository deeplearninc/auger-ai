from auger.cli.cli import cli


class TestDataSetCLI():
    def test_list(self, runner, log, isolated):
        result = runner.invoke(cli, ['dataset', 'list'])
        assert result.exit_code == 0

    def test_create(self, runner, log, isolated):
        result = runner.invoke(cli, ['dataset', 'create'])
        assert result.exit_code == 0

    def test_delete(self, runner, log, isolated):
        result = runner.invoke(cli, ['dataset', 'delete', 'test'])
        assert result.exit_code == 0

    def test_select(self, runner, log, isolated):
        result = runner.invoke(cli, ['dataset', 'select', 'iris'])
        assert result.exit_code == 0
