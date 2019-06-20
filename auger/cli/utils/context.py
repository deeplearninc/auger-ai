import os
import sys
import click
import logging

from auger.api.credentials import Credentials
from a2ml.api.auger.hub.rest_api import RestApi
from auger.cli.utils.config_yaml import ConfigYaml

log = logging.getLogger("auger")

CONTEXT_SETTINGS = dict(auto_envvar_prefix='AUGER')


class Context(object):

    def __init__(self, name=''):
        super(Context, self).__init__()
        self.load_config()
        if len(name) > 0:
            name = "{:<9}".format('[%s]' % name)
        self.name = name
        self.debug = self.config['auger'].get('debug', False)
        self.credentials = Credentials(self.config['auger']).load()
        RestApi().setup(self, self.credentials.api_url, self.credentials.token)

    def copy(self, name):
        new = Context(name)
        new.config = self.config
        return new

    def log(self, msg, *args, **kwargs):
        log.info('%s%s' %(self.name, msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        log.debug('%s%s' %(self.name, msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        log.error('%s%s' %(self.name, msg), *args, **kwargs)

    def load_config(self, path=None):
        self.config = {}
        if path is None:
            path = os.getcwd()
        self.config['auger'] = self._load_config(
             os.path.abspath(os.path.join(path, 'auger.yaml')))

    def _load_config(self, name):
        config = ConfigYaml()
        if os.path.isfile(name):
            config.load_from_file(name)
        return config

    @staticmethod
    def setup_logger(format='%(asctime)s %(name)s | %(message)s'):
        logging.basicConfig(
            stream=sys.stdout,
            datefmt='%H:%M:%S',
            format=format,
            level=logging.INFO)


pass_context = click.make_pass_decorator(Context, ensure=True)
