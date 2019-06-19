import logging
import shutil
import os

import pytest
from click.testing import CliRunner


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
    # os.chdir('test_project')
