from auger.cli.cli import cli
from .utils import CliRunnerMixin


class TestModelCLI(CliRunnerMixin):
    def test_deploy(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['model', 'deploy'])
        assert result.exit_code == 0


    def test_predict(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['model', 'predict'])
        assert result.exit_code == 0

