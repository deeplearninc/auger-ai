from a2ml.api.auger.hub.project import AugerProjectApi
from a2ml.api.auger.hub.org import AugerOrganizationApi
from a2ml.api.auger.hub.utils.exception import AugerException


class Project(AugerProjectApi):
    """Auger Cloud Projects(s) management"""

    def __init__(self, ctx, project_name=None):
        self.ctx = ctx
        org = AugerOrganizationApi(ctx.credentials.organisation)
        if org.properties() is None:
            raise AugerException('Can\'t find organization %s' % \
                ctx.credentials.organisation)
        super(Project, self).__init__(org, project_name)
