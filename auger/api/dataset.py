from a2ml.api.auger.hub.data_set import AugerDataSetApi


class DataSet(AugerDataSetApi):
    """Auger Cloud Data Set(s) management"""

    def __init__(self, ctx, project, data_set_name=None):
        super(DataSet, self).__init__(project, data_set_name)
        self.project = project
        self.ctx = ctx

    def create(self, data_source_file, data_set_name=None):
        AugerDataSetApi.verify(data_source_file)
        if not self.project.is_running():
            self.ctx.log('Starting Project to process request...')
            self.project.start()
        super().create(data_source_file, data_set_name)
        return self
