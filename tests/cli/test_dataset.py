from auger.cli.cli import cli
from .utils import CliRunnerMixin


class TestDataSetCLI(CliRunnerMixin):
    def test_list(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['dataset', 'list'])
        assert result.exit_code == 0

    def test_create(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['dataset', 'create'])
        assert result.exit_code == 0

    def test_delete(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['dataset', 'delete', 'test'])
        assert result.exit_code == 0

    def test_select(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['dataset', 'select', 'test'])
        assert result.exit_code == 0
