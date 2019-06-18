from auger.cli.cli import cli
from .utils import CliRunnerMixin


class TestExperimentCLI(CliRunnerMixin):
    def test_list(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'list'])
        assert result.exit_code == 0


    def test_start(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code == 0


    def test_status(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'status'])
        assert result.exit_code == 0


    def test_stop(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'stop'])
        assert result.exit_code == 0


    def test_leaderboard(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'leaderboard'])
        assert result.exit_code == 0


    def test_history(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['experiment', 'history'])
        assert result.exit_code == 0

