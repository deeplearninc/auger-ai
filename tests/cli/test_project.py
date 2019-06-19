from auger.cli.cli import cli


class TestProjectCLI():
    def test_list(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0

    def test_create(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'create', 'test'])
        assert result.exit_code == 0

    def test_delete(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'delete', 'test'])
        assert result.exit_code == 0

    def test_select(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'select', 'test'])
        assert result.exit_code == 0

    def test_start(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0

    def test_stop(self, runner, isolated):
        result = runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0
