import click

from auger.api.datasource import AugerDataSource
from auger.cli.utils.context import pass_context

class DataSourceCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def list(self):
        AugerDataSource(self.ctx).list()

    def create(self, *args, **kwargs):
        AugerDataSource(self.ctx).create(*args, **kwargs)

    def delete(self, *args, **kwargs):
        AugerDataSource(self.ctx).delete(*args, **kwargs)


@click.group('datasource', short_help='Auger data source management')
@pass_context
def command(ctx):
    """Auger data source management"""
    ctx.setup_logger(format='')

@click.command(short_help='List Auger datasources')
@pass_context
def list_cmd(ctx):
    """List Auger datasources"""
    DataSourceCmd(ctx).list()

@click.command(short_help='Create Auger data source on the Hub')
@pass_context
def create_cmd(ctx):
    """Create Auger data source on the Hub"""
    DataSourceCmd(ctx).create()

@click.command(short_help='Delete Auger data source on the Hub')
@pass_context
def delete_cmd(ctx):
    """Delete Auger data source on the Hub"""
    DataSourceCmd(ctx).delete()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd)
    command.add_command(create_cmd)
    command.add_command(delete_cmd)

add_commands()
