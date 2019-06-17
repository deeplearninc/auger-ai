from auger.api.project import Project

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

def with_project(decorated):
    def wrapper(self, *args, **kwargs):
        project_name = self.ctx.config['auger'].get('project', None)
        if project_name is None:
            raise Exception(
                'Please specify your project name (auger.yaml/project)...')
        project = Project(self.ctx, project_name)
        return decorated(self, project, *args, **kwargs)
    return wrapper
