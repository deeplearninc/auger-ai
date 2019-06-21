import pytest

from auger.cli.cli import cli
from auger.api.cloud.rest_api import RestApi
from auger.api.credentials import Credentials


class PatchedCreds():
    token = 'fake_token'
    username = 'test_username@example.com'
    organisation = 'test_organisation'
    api_url = 'https://example.com'

    def save(self):
        pass


class AnonymousCreds():
    token = None
    username = None
    organisation = None
    api_url = None


def load_logged_user(*args, **kwargs):
    return PatchedCreds()


def load_anonymous_user(*args, **kwargs):
    return AnonymousCreds()


class TestAuthCLI():
    def test_login(self, log, runner, isolated, monkeypatch):
        def login_mock(self, method, *args, **kwargs):
            return {
                'create_token': {
                    'data': {
                        'token': 'fake_token_for_testing_purpose',
                        },
                },
                'get_organizations': {
                    'meta': {
                        'status': 200, 
                        'pagination': 
                            {'limit': 100, 'total': 1, 'count': 1, 'offset': 0}
                    }, 
                    'data': [{'name': 'auger'}]
                }
            }[method]
            raise NotImplementedError("Trying to access not implemented method: %s" % method)
        monkeypatch.setattr(RestApi, 'call_ex', login_mock)
        monkeypatch.setattr(Credentials, 'save', lambda a: None)
        result = runner.invoke(
            cli,
            ['auth', 'login'],
            input="test@example.com\nauger\npassword\n")
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "You are now logged in on https://app.auger.ai"
                " as test@example.com.")

    def test_logout(self, log, runner, isolated, monkeypatch):
        monkeypatch.setattr(Credentials, 'load', load_logged_user)
        monkeypatch.setattr(Credentials, 'verify', lambda x: True)
        result = runner.invoke(cli, ['auth', 'logout'])
        assert result.exit_code == 0
        assert log.records[-1].message == "You are logged out of Auger."

    def test_whoami_anonymous(self, log, runner, monkeypatch):
        monkeypatch.setattr(Credentials, 'load', load_anonymous_user)
        result = runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code != 0
        assert (log.records[-1].message ==
                "Please login to Auger...")

    def test_whoami_authenticated(self, log, runner, monkeypatch):
        monkeypatch.setattr(Credentials, 'load', load_logged_user)
        monkeypatch.setattr(Credentials, 'save', lambda a: None)
        
        result = runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "test_username@example.com test_organisation https://example.com")

    def test_logout_not_logged(self, log, runner, isolated, monkeypatch):
        monkeypatch.setattr(Credentials, 'load', load_anonymous_user)
        monkeypatch.setattr(Credentials, 'save', lambda a: None)
        result = runner.invoke(cli, ['auth', 'logout'])
        assert (log.records[-1].message == 'You are not logged in Auger.')
        assert result.exit_code != 0
