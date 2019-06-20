from a2ml.api.auger.hub.data_set import AugerDataSetApi
from a2ml.api.auger.hub.utils.exception import AugerException


class DataSet(AugerDataSetApi):
    """Auger Cloud Data Set(s) management"""

    def __init__(self, ctx, project, data_set_name=None):
        if project is None:
            raise AugerException(
                'Project is required to construct DataSet object...')
        super(DataSet, self).__init__(project, data_set_name)
        self.project = project
        self.ctx = ctx

    def create(self, data_source_file):
        if data_source_file is None:
            raise AugerException('Please specify data source file...')
        AugerDataSetApi.verify(data_source_file)
        if not self.project.is_running():
            self.ctx.log('Starting Project to process request...')
            self.project.start()
        super().create(data_source_file, self.object_name)
        return self
