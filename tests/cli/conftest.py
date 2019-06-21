import logging
import shutil
import os

import pytest
from click.testing import CliRunner

from auger.api.credentials import Credentials
from auger.api.cloud.rest_api import RestApi


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def isolated(runner):
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def log(caplog):
    caplog.set_level(logging.INFO)
    return caplog


@pytest.fixture
def project(isolated):
    source = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'fixtures',
        'test_project')
    shutil.copytree(source, './test_project')


@pytest.fixture
def authenticated(monkeypatch):
    monkeypatch.setattr(Credentials, 'verify', lambda x: True)


@pytest.fixture(scope="function", autouse=True)
def rest_api_intercept(monkeypatch):
    def call_ex(self, *args, **kwargs):
        print(*args, **kwargs)
    monkeypatch.setattr(RestApi, 'call_ex', call_ex)
