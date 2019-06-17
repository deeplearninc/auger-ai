from a2ml.api.auger.hub.data_set import AugerDataSetApi


class DataSet(AugerDataSetApi):
    """Auger Cloud Data Set(s) management"""

    def __init__(self, project, data_set_name=None):
        super(DataSet, self).__init__(project, data_set_name)
