from a2ml.api.auger.hub.experiment import AugerExperimentApi
from a2ml.api.auger.hub.utils.exception import AugerException


class Experiment(AugerExperimentApi):
    """Auger Cloud Experiments(s) management"""

    def __init__(self, ctx, dataset, experiment_name=None):
        if dataset is None:
            raise AugerException(
                'DataSet is required to construct Experiment object...')
        super(Experiment, self).__init__(dataset.project, experiment_name)
        self.dataset = dataset
        self.ctx = ctx

    def list(self):
        data_set_id = self.dataset.oid
        filter_by_dataset = \
            lambda exp: exp.get('project_file_id') == data_set_id
        return (e for e in super().list() if filter_by_dataset(e))

    def start(self):
        if not self.dataset.is_exists:
            raise AugerException('Can\'t find DataSet on Auger Cloud...')

        if self.object_name and self.is_exists:
            data_set_id = self.dataset.oid
            experiment_data_set = self.properties().get('project_file_id')
            if data_set_id != experiment_data_set:
                raise AugerException('Can\'t start Experiment '
                    'configured with different DataSet...')

        if not self.dataset.project.is_running():
            self.ctx.log('Starting Project to process request...')
            self.dataset.project.start()

        if (self.object_name is None) or (not self.is_exists):
            self.create(self.dataset.name)
            self.ctx.log('Created Experiment %s ' % self.name)

        experiment_session_id = self.run()
        self.ctx.log('Started Experiment %s search...' % self.name)

        return self.name, experiment_session_id
