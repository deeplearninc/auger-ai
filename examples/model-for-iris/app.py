import logging
import os
import sys
import time

from auger.api.dataset import DataSet
from auger.api.model import Model
from auger.api.project import Project
from auger.api.experiment import Experiment, AugerExperimentSessionApi
from auger.api.utils.context import Context
from auger.cli.utils.config import AugerConfig


PREDICTION_SOURCE = 'files/iris_data_test.csv'
PREDICTION_TARGET = 'files/irist_data_set_predict.csv'
DATASET_NAME = 'iris.csv'

log = logging.getLogger('auger.ai')


class ExampleApp():
    def __init__(self, ctx):
        self.ctx = ctx
        def print_(*args, **kwargs):
            print(*args, **kwargs)
        self.ctx.log = print_
        self.dataset = None
        self.model_id = None
        self.project = Project(
            self.ctx, self.ctx.get_config('config').get('name', None))

    def _get_datasets(self):
        """return list of existing datasets in the Aguer Cloud"""
        dataset_list = []
        for dataset in iter(DataSet(self.ctx, self.project).list()):
            dataset_list.append(dataset['name'])
        return dataset_list

    def _start_experiment(self, experiment_name):
        eperiment_name, session_id = \
            Experiment(self.ctx, self.dataset, experiment_name).start()
        AugerConfig(self.ctx).set_experiment(eperiment_name, session_id)
        return session_id

    def _wait_for_experiment(self, session_id):
        AugerExperimentSessionApi(self.ctx, None, None, session_id).wait_for_status([
            'preprocess', 'started'])

    def prepare_dataset(self):
        """check whether dataset selected, if not, select or create one"""
        self.ctx.log("Checking dataset...")
        selected = self.ctx.get_config('config').get('dataset', None)
        if selected is None:
            if DATASET_NAME in self._get_datasets():
                # try to select existing
                AugerConfig(self.ctx).set_data_set(
                    DATASET_NAME, '').set_experiment(None)
                self.dataset = DataSet(self.ctx, self.project, DATASET_NAME)
            else:
                # or create new
                self.ctx.log("No dataset found, creating the first one...")
                source = self.ctx.get_config('config').get('source', None)
                dataset = DataSet(self.ctx, self.project).create(source)
                AugerConfig(self.ctx).set_data_set(
                    dataset.name, source).set_experiment(None)
                self.dataset = DataSet(self.ctx, self.project, dataset.name)
        else:
            self.dataset = DataSet(self.ctx, self.project, selected)
            self.ctx.log("Currently selected: %s" % selected)

    def run_experiment(self):
        experiment_name = self.ctx.get_config('auger').get(
            'experiment/name', None)
        # run_id = self.ctx.get_config('auger').get(
        #     'experiment/experiment_session_id', None)

        # if run_id is None or experiment_name is None:
            # if no experiment ran:
            # run_id = self._start_experiment(experiment_name)
        run_id = self._start_experiment(experiment_name)
        # else:
        #     # if experiment exists, (start if needed) and wait for it
        #     session_api = AugerExperimentSessionApi(
        #         self.ctx, None, None, run_id)
        #     status = session_api.properties().get('status')
        #     self.ctx.log('Experiment status is %s' % status)
        #     # available choices are:
        #     # [preprocess, started, completed, interrupted]
        #     if status not in ('preprocess', 'started'):
        #         run_id = self._start_experiment(experiment_name)
        # wait for experiment to stop
        self.ctx.log("waiting for experiment %s to finish" % experiment_name)
        self._wait_for_experiment(run_id)
        leaderboard, status = Experiment(
            self.ctx, self.dataset, experiment_name).leaderboard(run_id)
        self.model_id = leaderboard[0]['model id']

    def deploy(self):
        Model(self.ctx, self.project).deploy(self.model_id, locally=True)

    def predict(self):
        if os.path.exists(PREDICTION_TARGET):
            self.ctx.log(
                "Prediction already exists."
                " If you want to re-run predict, just delete prediction file: " %
                PREDICTION_TARGET)
        else:
            Model(self.ctx, self.project).predict(
                PREDICTION_SOURCE, self.model_id, locally=True)


def main():
    context = Context()
    try:
        app = ExampleApp(context)
        app.prepare_dataset()
        app.run_experiment()
        app.deploy()
        app.predict()
    except Exception as e:
        import traceback; traceback.print_exc();
        context.log(
            "Example application execution has failed with error: '%s'" %
            str(e))


if __name__ == '__main__':
    main()
