from .base import *

from .production import *

try:
    from .local import *    # Change this to production when you go Live
except:
    pass
