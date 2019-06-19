import os
import click
import urllib.parse

from auger.api.dataset import DataSet
from auger.api.experiment import Experiment
from auger.cli.utils.config import AugerConfig
from auger.cli.utils.context import pass_context
from auger.cli.utils.decorators import \
    error_handler, authenticated, with_project, with_dataset

class ExperimentCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    @error_handler
    @authenticated
    @with_dataset
    def list(self, dataset):
        count = 0
        for exp in iter(Experiment(self.ctx, dataset).list()):
            self.ctx.log(exp.get('name'))
            count += 1
        self.ctx.log('%s Experiment(s) listed' % str(count))

    @error_handler
    @authenticated
    @with_dataset
    def start(self, dataset):
        experiment_name = self.ctx.config['auger'].get('experiment/name', None)
        eperiment_name, session_id = \
            Experiment(self.ctx, dataset, experiment_name).start()
        AugerConfig(self.ctx).set_experiment(eperiment_name, session_id)

    def status(self, *args, **kwargs):
        Experiment(self.ctx).status(*args, **kwargs)

    def stop(self, *args, **kwargs):
        Experiment(self.ctx).stop(*args, **kwargs)

    def leaderboard(self, *args, **kwargs):
        Experiment(self.ctx).leaderboard(*args, **kwargs)

    def history(self, *args, **kwargs):
        Experiment(self.ctx).history(*args, **kwargs)


@click.group('experiment', short_help='Auger experiment management')
@pass_context
def command(ctx):
    """Auger experiment management"""
    ctx.setup_logger(format='')

@click.command(short_help='List Experiments for selected DataSet')
@pass_context
def list_cmd(ctx):
    """List Experiments for selected DataSet"""
    ExperimentCmd(ctx).list()

@click.command(short_help='Start Experiment')
@pass_context
def start(ctx):
    """Start Experiment.
       If Experiment is not selected, new Experiment will be created.
    """
    ExperimentCmd(ctx).start()

@click.command(short_help='Check Experiment\'s status')
@pass_context
def status(ctx):
    """Check Experiment\'s status"""
    ExperimentCmd(ctx).status()


@click.command(short_help='Stop Experiment')
@pass_context
def stop(ctx):
    """Stop Experiment"""
    ExperimentCmd(ctx).stop()

@click.command(short_help='Show Experiment leaderboard')
@pass_context
def leaderboard(ctx):
    """Show Experiment leaderboard"""
    ExperimentCmd(ctx).leaderboard()

@click.command(short_help='Show Experiment history')
@pass_context
def history(ctx):
    """Show Experiment history"""
    ExperimentCmd(ctx).history()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd, name='list')
    command.add_command(start)
    command.add_command(status)
    command.add_command(stop)
    command.add_command(leaderboard)
    command.add_command(history)

add_commands()
