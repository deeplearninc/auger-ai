import re
import ruamel.yaml

from auger.api.utils import fsclient


class ConfigYaml(object):
    def __init__(self):
        super(ConfigYaml, self).__init__()
        self.filename = None
        self.yaml = None

    def load_from_file(self, filename):
        if not isinstance(filename, str) or len(filename) == 0:
            raise ValueError("please provide yaml file name")
        self.filename = filename
        with fsclient.open_file(filename, 'r') as f:
            self.yaml = ruamel.yaml.load(f,
                Loader=ruamel.yaml.RoundTripLoader)
        return self

    def get(self, path, default=None):
        options = self.yaml
        if (options == None):
            return default

        path = path.split('/')
        for opt in path:
            if opt in options:
                options = options[opt]
            else:
                return default

        if options is None:
            options = default
        return options

    def set(self, path, value):
        options = self.yaml
        path = path.split('/')
        for opt in path[0:-1]:
            options = options[opt]
        options[path[-1]] = value

    def write(self, filename=None):
        filename = filename if filename else self.filename
        fsclient.write_text_file(filename, ruamel.yaml.dump(self.yaml,
                Dumper=ruamel.yaml.RoundTripDumper))
        
        # with open(self.filename, 'w') as out:
        #     out.write(ruamel.yaml.dump(self.yaml,
        #         Dumper=ruamel.yaml.RoundTripDumper))
