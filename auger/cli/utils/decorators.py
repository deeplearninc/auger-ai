from functools import wraps
from auger.api.project import Project
from auger.api.dataset import DataSet
from a2ml.api.auger.cloud.utils.exception import AugerException


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

def _get_project(self, autocreate):
    project_name = self.ctx.get_config('auger').get('project', None)
    if project_name is None:
        raise AugerException(
            'Please specify project name in auger.yaml/project...')
    project = Project(self.ctx, project_name)
    project_properties = project.properties()
    if project_properties is None:
        if autocreate:
            self.ctx.log(
                'Can\'t find project %s on the Auger Cloud. '
                'Creating...' % project_name)
            project.create()
        else:
            raise AugerException('Can\'t find project %s' % project_name)
    return project

def with_project(autocreate=False):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            project = _get_project(self, autocreate)
            return decorated(self, project, *args, **kwargs)
        return wrapper
    return decorator

def with_dataset(decorated):
    def wrapper(self, *args, **kwargs):
        project = _get_project(self)
        data_set_name = self.ctx.get_config('auger').get('dataset', None)
        if data_set_name is None:
            raise AugerException(
                'Please specify dataset name in auger.yaml/dataset...')
        dataset = DataSet(self.ctx, project, data_set_name)
        return decorated(self, dataset, *args, **kwargs)
    return wrapper
