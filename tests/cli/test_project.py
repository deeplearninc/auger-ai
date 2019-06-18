from auger.cli.cli import cli


class TestProjectCLI():
    def test_list(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0

    def test_create(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'create', 'test'])
        assert result.exit_code == 0

    def test_delete(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'delete', 'test'])
        assert result.exit_code == 0

    def test_select(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'select', 'test'])
        assert result.exit_code == 0

    def test_start(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0

    def test_stop(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0

