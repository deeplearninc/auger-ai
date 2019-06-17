from a2ml.api.auger.hub.project import AugerProjectApi
from a2ml.api.auger.hub.org import AugerOrganizationApi


class Project(AugerProjectApi):
    """Auger Cloud Projects(s) management"""

    def __init__(self, ctx, project_name=None):
        self.ctx = ctx
        super(Project, self).__init__(
            AugerOrganizationApi(ctx.credentials.organisation), project_name)
        # patch request path
        self._set_api_request_path('AugerProjectApi')
        # load project id
        self.object_id = self.properties().get('id')
