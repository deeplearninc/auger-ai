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

    def verify(self, *a, **kwa): return True


class TestProjectCLI():
    def test_list(self, runner, log, monkeypatch):
        # PAYLOAD = {
        #     'get_organizations': {
        #         'meta': {
        #             'status': 200, 
        #             'pagination': 
        #                 {'limit': 100, 'total': 1, 'count': 1, 'offset': 0}
        #         }, 
        #         'data': [{'name': 'auger'}]
        #     },
        #     'get_projects': {
        #         'meta': {
        #             'status': 200,
        #             'pagination': {
        #                 'count': 31, 'limit': 100, 'offset': 0, 'total': 31}},
        #         'data': [{
        #           "object": "project",
        #           "deleted": False,
        #           "id": 1,
        #           "name": "project_1",}]
        #     }
        # }
        # def dispatcher(self, method, *args, **kwargs):
        #     print("DISPATHEC")
        #     return PAYLOAD[method]
        # monkeypatch.setattr(
        #     RestApi, 'call_ex', lambda x, *args, **kwargs: dispatcher(x, *args, **kwargs))
        # monkeypatch.setattr(Credentials, 'load', PatchedCreds())
        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0
        print(log.messages[-1])

    def test_create(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['project', 'create', 'test'])
        assert result.exit_code == 0
        print(log.messages[-1])

    def test_delete(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['project', 'delete', 'test'])
        assert result.exit_code == 0
        print(log.messages[-1])

    def test_select(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['project', 'select', 'test'])
        assert result.exit_code == 0
        print(log.messages[-1])

    def test_start(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0
        print(log.messages[-1])

    def test_stop(self, log, runner, isolated, authenticated):
        result = runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0
        print(log.messages[-1])
