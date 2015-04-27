import pkg_resources, random

from omnomnom.common.wordgen.names import FullNameGenerator

class EmailGenerator(object):
    FORMATS = {
        'first_last': "{first_name}_{last_name}",
        'first.last': "{first_name}.{last_name}",
        'last_first': "{last_name}_{first_name}",
        'flast': "{first_initial}{last_name}",
        'firstl': "{first_name}{last_initial}",
        'first0': "{first_name}{digit}",
        'first95': "{first_name}{year}",
        'flast0': "{first_initial}{last_name}{digit}",
        'flast95': "{first_initial}{last_name}{year}",
        }
    def __init__(self, domain='omnomnom.email'):
        self.domain = domain
        self.namegen = FullNameGenerator.instance()

    def _gen_digit(self):
        return random.choice(list(range(10)))
        
    def generate(self, force_format=None):
        if force_format:
            fmt = self.FORMATS[force_format]
        else:
            fmt = self.FORMATS[random.choice(list(self.FORMATS.keys()))]

        first_name, mi, last_name = self.namegen.get_name()
        email = fmt.format(first_name=first_name,
                           last_name=last_name,
                           first_initial=first_name[0],
                           last_initial=last_name[0],
                           digit=self._gen_digit(),
                           year='9'+str(self._gen_digit()),
                           )
        email += '@' + self.domain
        email = email.lower()
        return email
            
    _INSTANCE = None
    @classmethod
    def instance(cls):
        if not cls._INSTANCE:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    
