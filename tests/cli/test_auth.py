from auger.cli.cli import cli


class TestAuthCLI():
    def test_login(self, log, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ['auth', 'login'],
                input="test@example.com\nauger\npassword\n")
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "You are now logged in on https://app.auger.ai"
                " as test@example.com.")

    def test_logout(self, log, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ['auth', 'login'],
                input="test@example.com\nauger\npassword\n")
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['auth', 'logout'])
            assert result.exit_code == 0
            assert log.records[-1].message == "You are logged out of Auger."

    def test_whoami(self, log, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ['auth', 'login'],
                input="test@example.com\nauger\npassword\n")
        result = runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "test@example.com auger https://app.auger.ai")

    def test_logout_not_logged(self, log, runner, isolated):
        result = runner.invoke(cli, ['auth', 'logout'])
        assert (log.records[-1].message == 'You are not logged in Auger.')
