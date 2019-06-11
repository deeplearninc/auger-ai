import os
import errno
import click

from auger.hub_api_client import HubApiClient

from .utils.context import pass_context
from .auger.credentials import Credentials
from .auger.hub.auth import AugerAuthApi
from .hub.utils.exception import AugerException


class AuthCmd(object):

     def __init__(self, ctx):
        self.ctx = ctx
        self.credentials = Credentials(ctx.config['auger']).load()

    def whoami(self):
        if self.credentials.token is None:
            self.ctx.log('Please login to Auger...')
        else:
            self.ctx.log(
                '%s %s %s' % (
                    self.credentials.username,
                    self.credentials.organisation,
                    self.credentials.api_url))


    def login(self, username, password, organisation, url=None):
        try:
            self.credentials.token = None
            self.credentials.save()

            if url is None:
                url = self.credentials.api_url

            token = AugerAuthApi().login(
                self.ctx, username, password, organisation, url)

            self.credentials.token = token
            self.credentials.username = username
            self.credentials.api_url = url
            self.credentials.organisation = organisation
            self.credentials.save()

            self.ctx.log(
                'You are now logged in on %s as %s.' % (url, username))

        except Exception as exc:
            exc_text = str(exc)
            if 'Email or password incorrect' in exc_text:
                exc_text = 'Email or password incorrect...'
            self.ctx.log(exc_text)

    def logout(self):
        if self.credentials.token is None:
            self.ctx.log('You are not loged in Auger.')
        else:
            self.credentials.token = None
            self.credentials.api_url = None
            self.credentials.organisation = None
            self.credentials.save()
            self.ctx.log('You are loged out of Auger.')


@click.command('whoami', short_help='Display the current logged in user')
@pass_context
def command(ctx):
    """Create new A2ML project."""
    ctx.setup_logger(format='')
    AuthCmd(ctx, project_name).whoami()
