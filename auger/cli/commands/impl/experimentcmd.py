from auger.api.experiment import Experiment
from auger.cli.utils.config import AugerConfig
from auger.cli.utils.formatter import print_table
from auger.cli.utils.decorators import \
    error_handler, authenticated, with_dataset
from auger.api.cloud.utils.exception import AugerException


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
        return {'experiments': Experiment(self.ctx, dataset).list()}

    @error_handler
    @authenticated
    @with_dataset
    def start(self, dataset):
        experiment_name = \
            self.ctx.config.get('experiment/name', None)
        eperiment_name, session_id = \
            Experiment(self.ctx, dataset, experiment_name).start()
        AugerConfig(self.ctx).set_experiment(eperiment_name, session_id)
        return {'eperiment_name': eperiment_name, 'session_id': session_id}

    @error_handler
    @authenticated
    @with_dataset
    def stop(self, dataset):
        name = self.ctx.config.get('experiment/name', None)
        if name is None:
            raise AugerException('Please specify Experiment name...')
        if Experiment(self.ctx, dataset, name).stop():
            self.ctx.log('Search is stopped...')
        else:
            self.ctx.log('Search is not running. Stop is ignored.')
        return {'stopped': name}

    @error_handler
    @authenticated
    @with_dataset
    def leaderboard(self, dataset, run_id = None):
        name = self.ctx.config.get('experiment/name', None)
        if name is None:
            raise AugerException('Please specify Experiment name...')
        if run_id is None:
            run_id = self.ctx.config.get(
                'experiment/experiment_session_id', None)
        leaderboard, status, run_id = Experiment(
            self.ctx, dataset, name).leaderboard(run_id)
        if leaderboard is None:
            raise AugerException('No leaderboard was found...')
        self.ctx.log('Leaderboard for Run %s' % run_id)
        print_table(self.ctx.log, leaderboard[::-1])
        messages = {
            'preprocess': 'Search is preprocessing data for traing...',
            'started': 'Search is in progress...',
            'completed': 'Search is completed.',
            'interrupted': 'Search was interrupted.'
        }
        message = messages.get(status, None)
        if message:
            self.ctx.log(message)
        else:
            self.ctx.log('Search status is %s' % status)
        return {'run_id': run_id, 'leaderboard': leaderboard, 'status': status}

    @error_handler
    @authenticated
    @with_dataset
    def history(self, dataset):
        name = self.ctx.config.get('experiment/name', None)
        if name is None:
            raise AugerException('Please specify Experiment name...')
        for exp_run in iter(Experiment(self.ctx, dataset, name).history()):
            self.ctx.log("run id: {}, start time: {}, status: {}".format(
                exp_run.get('id'),
                exp_run.get('model_settings').get('start_time'),
                exp_run.get('status')))
        return {'history': Experiment(self.ctx, dataset, name).history()}
