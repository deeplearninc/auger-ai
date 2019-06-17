from functools import wraps
from auger.api.project import Project
from a2ml.api.auger.hub.utils.exception import AugerException


def error_handler(decorated):
    def wrapper(self, *args, **kwargs):
        try:
            return decorated(self, *args, **kwargs)
        except Exception as exc:
            if self.ctx.debug:
                import traceback
                traceback.print_exc()
            self.ctx.log(str(exc))
    return wrapper

def authenticated(decorated):
    def wrapper(self, *args, **kwargs):
        # verify avalability of auger credentials
        self.ctx.credentials.verify()
        return decorated(self, *args, **kwargs)
    return wrapper

def with_project(autocreate=False):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            project_name = self.ctx.config['auger'].get('project', None)
            if project_name is None:
                raise AugerException(
                    'Please specify your project name (auger.yaml/project)...')
            project = Project(self.ctx, project_name)
            project_properties = project.properties()
            if project_properties is None:
                if autocreate:
                    self.ctx.log(
                        'Can\'t find project %s on the Auger Cloud.'
                        ' Creating...' % project_name)
                    project.create()
                else:
                    raise AugerException('Can\'t find project %s' % project_name)
            return decorated(self, project, *args, **kwargs)
        return wrapper
    return decorator    
