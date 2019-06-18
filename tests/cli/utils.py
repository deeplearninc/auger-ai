from click.testing import CliRunner


class CliRunnerMixin():
    def setup_method(self):
        self.runner = CliRunner()
