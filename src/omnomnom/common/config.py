import json

_NO_DEFAULT = object()
class Configuration(object):
    def __init__(self, config_path):
        self.reload_data(config_path)

    def reload_data(self, config_path=None):
        if config_path:
            self.config_path = config_path
        with open(self.config_path) as f:
            self.config_data = f.read()
        self.config = json.loads(self.config_data)

    def get(self, *args, default=_NO_DEFAULT):
        current = self.config
        
        for arg in args:
            if arg in current:
                current = current[arg]
            elif default is not _NO_DEFAULT:
                return default
            else:
                raise KeyError("Missing key %s as part of %s" % (arg, args))

        return current
