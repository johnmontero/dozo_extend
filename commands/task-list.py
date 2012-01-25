
from dozo.config    import get_config_value
from dozo.commands  import BaseCommand, CommandError

import envoy

class Command(BaseCommand):
    """
    Lists all task.
    """
    
    # command information
    usage = '--task-list'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
    
    def handle(self):
        r = envoy.run('task list')
        if r.status_code == 0:
	    print r.std_out
   	else:
	    print r.std_err
