from auger.api.project import Project
from auger.api.dataset import DataSet
from auger.api.utils.context import Context

ctx = Context()
ctx.setup_logger(format='')

project = Project(ctx, 'iris_project')
if not project.is_exists:
    project.create()
    ctx.log('Created project %s' % project.name)

for dataset in iter(DataSet(ctx, project).list()):
    ctx.log(dataset.get('name'))

dataset = DataSet(ctx, project).create('iris.csv')
ctx.log('Created dataset %s' % dataset.name)
