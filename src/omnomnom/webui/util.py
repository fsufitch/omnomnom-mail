import random, string

from jinja2 import Environment, PackageLoader

TEMPLATE_ENVIRONMENT = None
def init_template_environment():
    global TEMPLATE_ENVIRONMENT
    if not TEMPLATE_ENVIRONMENT:
        TEMPLATE_ENVIRONMENT = Environment(loader=PackageLoader("omnomnom.webui", "templates"))

class apply_template(object):
    ''' Decorator; Apply template decorator '''
    def __init__(self, tmpl_name):
        if not TEMPLATE_ENVIRONMENT:
            init_template_environment()
        self.template = TEMPLATE_ENVIRONMENT.get_template(tmpl_name)

    def __call__(self, func):
        def _apply_template(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) is str:
                return result
            elif type(result) is dict:
                return self.template.render(**result)
            else:
                return result
        return _apply_template

def write_return(func):
    ''' Decorator; Apply self.write to whatever function is decorated '''
    def _write_return(_self, *args, **kwargs):
        result = func(_self, *args, **kwargs)
        if type(result) in (str, bytes):
            _self.write(result)
    return _write_return
