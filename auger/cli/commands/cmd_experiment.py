import click

from auger.api.experiment import AugerExperiment
from auger.cli.utils.context import pass_context

class ExperimentCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def list(self):
        AugerExperiment(self.ctx).list()

    def start(self, *args, **kwargs):
        AugerExperiment(self.ctx).start(*args, **kwargs)

    def status(self, *args, **kwargs):
        AugerExperiment(self.ctx).status(*args, **kwargs)

    def stop(self, *args, **kwargs):
        AugerExperiment(self.ctx).stop(*args, **kwargs)

    def leaderboard(self, *args, **kwargs):
        AugerExperiment(self.ctx).leaderboard(*args, **kwargs)

    def history(self, *args, **kwargs):
        AugerExperiment(self.ctx).history(*args, **kwargs)


@click.group('experiment', short_help='Auger experiment management')
@pass_context
def command(ctx):
    """Auger experiment management"""
    ctx.setup_logger(format='')

@click.command(short_help='List experiments')
@pass_context
def list_cmd(ctx):
    """List Auger experiments"""
    ExperimentCmd(ctx).list()

@click.command(short_help='Run experiment')
@pass_context
def start_cmd(ctx):
    """Start Auger experiment"""
    ExperimentCmd(ctx).start()

@click.command(short_help='Check experiment\'s status')
@pass_context
def status_cmd(ctx):
    """CHeck experiment\'s status"""
    ExperimentCmd(ctx).status()


@click.command(short_help='Stop experiment')
@pass_context
def stop_cmd(ctx):
    """Stop experiment"""
    ExperimentCmd(ctx).stop()

@click.command(short_help='Show experiment leaderboard')
@pass_context
def leaderboard_cmd(ctx):
    """Show experiment leaderboard"""
    ExperimentCmd(ctx).leaderboard()

@click.command(short_help='Show experiment history')
@pass_context
def history_cmd(ctx):
    """Show experiment history"""
    ExperimentCmd(ctx).history()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd)
    command.add_command(start_cmd)
    command.add_command(status_cmd)
    command.add_command(stop_cmd)
    command.add_command(leaderboard_cmd)
    command.add_command(history_cmd)

add_commands()
