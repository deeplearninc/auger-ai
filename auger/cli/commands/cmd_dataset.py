import click

from auger.api.dataset import DataSet
from auger.cli.utils.context import pass_context
from auger.cli.utils.decorators import error_handler, authenticated, with_project

class DataSetCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    @error_handler
    @authenticated
    @with_project
    def list(self, project):
        for dataset in iter(DataSet(project).list()):
            self.ctx.log(dataset.get('name'))

    @error_handler
    @authenticated
    @with_project
    def create(self, project, source):
        if source is None:
            source = self.ctx.config['auger'].get('dataset/source')
        DataSet(self.ctx).create(*args, **kwargs)

    def delete(self, *args, **kwargs):
        DataSet(self.ctx).delete(*args, **kwargs)


@click.group('dataset', short_help='Auger Cloud dataset(s) management')
@pass_context
def command(ctx):
    """Auger Cloud data sets management"""
    ctx.setup_logger(format='')

@click.command(short_help='List data sets on Auger Cloud')
@pass_context
def list_cmd(ctx):
    """List Auger remote datasets"""
    DataSetCmd(ctx).list()

@click.command(short_help='Create data set on the Auger Cloud')
@click.option('--source', '-s',  default=None, type=click.STRING,
    help='Data source local file or remote url.')
@pass_context
def create(ctx):
    """Create data set on the Auger Cloud"""
    DataSetCmd(ctx).create(source)

@click.command(short_help='Delete data set on the Auger Cloud')
@pass_context
def delete(ctx):
    """Delete data set on the Auger Cloud"""
    DataSetCmd(ctx).delete()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd, name='list')
    command.add_command(create)
    command.add_command(delete)

add_commands()
