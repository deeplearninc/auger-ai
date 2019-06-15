import click

from auger.api.model import AugerModel
from auger.cli.utils.context import pass_context

class ModelCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def deploy(self):
        AugerModel(self.ctx).deploy()

    def create(self, *args, **kwargs):
        AugerModel(self.ctx).create(*args, **kwargs)


@click.group('model', short_help='Auger model management')
@pass_context
def command(ctx):
    """Auger model management"""
    ctx.setup_logger(format='')

@click.command(short_help='Deploy model')
@pass_context
def deploy_cmd(ctx):
    """Deploy Auger projects"""
    ModelCmd(ctx).deploy()

@click.command(short_help='Predict using deployed model')
@pass_context
def predict_cmd(ctx):
    """Create Auger model on the Hub"""
    ModelCmd(ctx).create()


@pass_context
def add_commands(ctx):
    command.add_command(deploy_cmd)
    command.add_command(predict_cmd)

add_commands()
