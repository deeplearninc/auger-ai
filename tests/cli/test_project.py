from auger.cli.cli import cli
from .utils import CliRunnerMixin


class TestProjectCLI(CliRunnerMixin):
    def test_list(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0

    def test_create(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'create', 'test'])
        assert result.exit_code == 0

    def test_delete(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'delete', 'test'])
        assert result.exit_code == 0

    def test_select(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'select', 'test'])
        assert result.exit_code == 0

    def test_start(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0

    def test_stop(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0

