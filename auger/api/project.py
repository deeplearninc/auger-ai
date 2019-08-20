from .cloud.project import AugerProjectApi
from .cloud.org import AugerOrganizationApi
from .cloud.utils.exception import AugerException


class Project(AugerProjectApi):
    """Auger Cloud Projects(s) management"""

    def __init__(self, ctx, project_name=None):
        if isinstance(ctx.credentials.organization, int):
            org_name = None
            org_id = ctx.credentials.organization
        else:
            org_name = ctx.credentials.organization
            org_id = None

        org = AugerOrganizationApi(ctx, org_name, org_id)
        super(Project, self).__init__(ctx, org, project_name)
