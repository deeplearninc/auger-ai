import click

from auger.api.dataset import DataSet
from auger.cli.utils.context import pass_context

class DataSetCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def list(self):
        DataSet(self.ctx).list()

    def create(self, *args, **kwargs):
        DataSet(self.ctx).create(*args, **kwargs)

    def delete(self, *args, **kwargs):
        DataSet(self.ctx).delete(*args, **kwargs)


@click.group('dataset', short_help='Auger Cloud dataset(s) management')
@pass_context
def command(ctx):
    """Auger Cloud data sets management"""
    ctx.setup_logger(format='')

@click.command(short_help='List data sets the Auger Cloud')
@pass_context
def list_cmd(ctx):
    """List Auger remote datasets"""
    DataSetCmd(ctx).list()

@click.command(short_help='Create data set on the Auger Cloud')
@pass_context
def create_cmd(ctx):
    """Create data set on the Auger Cloud"""
    DataSetCmd(ctx).create()

@click.command(short_help='Delete data set on the Auger Cloud')
@pass_context
def delete_cmd(ctx):
    """Delete data set on the Auger Cloud"""
    DataSetCmd(ctx).delete()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd)
    command.add_command(create_cmd)
    command.add_command(delete_cmd)

add_commands()
