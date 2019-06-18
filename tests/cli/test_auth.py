import logging

import vcr
from click.testing import CliRunner

from auger.cli.cli import cli
from .utils import CliRunnerMixin


my_vcr = vcr.VCR(
    cassette_library_dir='tests/fixtures/cassettes',
    filter_headers=['authorization'],
    record_mode='none',
    )


class TestAuthCLI(CliRunnerMixin):

    @my_vcr.use_cassette('login.yaml')
    def test_login(self, caplog):
        caplog.set_level(logging.INFO)
        result = self.runner.invoke(
            cli,
            ['auth', 'login'],
            input="test@example.com\nauger\npassword\n")
        assert result.exit_code == 0
        assert (caplog.records[-1].message ==
                "You are now logged in on https://app.auger.ai"
                " as test@example.com.")

    @my_vcr.use_cassette('logout.yaml')
    def test_logout(self, caplog):
        caplog.set_level(logging.INFO)
        result = self.runner.invoke(
            cli,
            ['auth', 'login'],
            input="test@example.com\nauger\npassword\n")
        result = self.runner.invoke(cli, ['auth', 'logout'])
        assert result.exit_code == 0
        assert caplog.records[-1].message == "You are loged out of Auger."

    @my_vcr.use_cassette('whoami.yaml')
    def test_whoami(self, caplog):
        caplog.set_level(logging.INFO)
        result = self.runner.invoke(
            cli,
            ['auth', 'login'],
            input="test@example.com\nauger\npassword\n")
        result = self.runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code == 0
        assert (caplog.records[-1].message ==
                "test@example.com auger https://app.auger.ai")
