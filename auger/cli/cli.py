import os
import sys

import click

from .utils.context import CONTEXT_SETTINGS, pass_context


class AugerCLI(click.MultiCommand):
    cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))

    def list_commands(self, ctx):
        command_list = []
        for filename in os.listdir(AugerCLI.cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                command_list.append(filename[4:-3])
        command_list.sort()
        return command_list

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('auger.cli.commands.cmd_' + name,
                             fromlist=[''])
        except ImportError as e:
            return
        return mod.command


@click.command(cls=AugerCLI, context_settings=CONTEXT_SETTINGS)
@pass_context
def cli(ctx):
    """Auger command line interface."""
