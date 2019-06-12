import os
import errno
import click

# TODO: implement auger project template
# from a2ml.cmdl.utils.template import Template
from .utils.context import CONTEXT_SETTINGS, pass_context


class NewCmd(object):

    def __init__(self, ctx, project_name):
        self.ctx = ctx
        self.project_name = project_name

    def mk_project_folder(self):
        project_path = os.path.abspath(os.path.join(os.getcwd(), self.project_name))
        try:
            os.makedirs(project_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise Exception('Can\'t create \'%s\'. Folder already exists.' % self.project_name)
            raise
        self.ctx.log('Created project folder %s', self.project_name)
        return project_path

    def create_project(self):
        try:
            project_path = self.mk_project_folder()
            Template.copy_config_files(project_path, ['config'] + PROVIDERS)
            # TODO: update help text
            self.ctx.log('To run experiment, please do: cd %s && a2ml train' % self.project_name)

        except Exception as e:
            self.ctx.log('%s', str(e))


@click.command('new', short_help='Create new auger project.')
@click.argument('project-name', required=True, type=click.STRING)
@pass_context
def command(ctx, project_name):
    """Create new auger project."""
    ctx.setup_logger(format='')
    NewCmd(ctx, project_name).create_project()
