import os
import shutil

class Template(object):

    @staticmethod
    def copy_config_files(experiment_path):
        module_path = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(os.path.abspath(os.path.join(module_path, '../template/'))):
            src_config = os.path.abspath(os.path.join(module_path, '../template/%s' % filename))
            dest_config = os.path.join(experiment_path, '%s' % filename)
            shutil.copy2(src_config, dest_config)
