import click

from auger.api.project import Project
from auger.cli.utils.context import pass_context

class ProjectCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def list(self):
        AugerProject(self.ctx).list()

    def create(self, *args, **kwargs):
        AugerProject(self.ctx).create(*args, **kwargs)

    def delete(self, *args, **kwargs):
        AugerProject(self.ctx).delete(*args, **kwargs)


@click.group('project', short_help='Auger project management')
@pass_context
def command(ctx):
    """Auger project management"""
    ctx.setup_logger(format='')

@click.command(short_help='List Auger projects')
@pass_context
def list_cmd(ctx):
    """List Auger projects"""
    ProjectCmd(ctx).list()

@click.command(short_help='Create Auger project on the Hub')
@pass_context
def create_cmd(ctx):
    """Create Auger project on the Hub"""
    ProjectCmd(ctx).create()

@click.command(short_help='Delete Auger project on the Hub')
@pass_context
def delete_cmd(ctx):
    """Delete Auger project on the Hub"""
    ProjectCmd(ctx).delete()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd)
    command.add_command(create_cmd)
    command.add_command(delete_cmd)

add_commands()
