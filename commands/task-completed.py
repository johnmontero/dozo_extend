
import datetime

from dozo.config    import get_config_value
from dozo.commands  import BaseCommand, CommandError

import envoy

class Command(BaseCommand):
    """
    Lists all task completed.
    """
    
    # command information
    usage = '--task-completed'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
    
    def handle(self):

        date = self.args.get_value('--task-completed') 
        if date is None:
            date = datetime.datetime.now().strftime('%m/%d/%Y')
        
        cmd = 'task _query status:completed project:today-work end:{0}'.format(date)
        r = envoy.run(cmd)
        if r.status_code == 0:            
            data = eval(r.std_out.replace('\n',''))
            tasks = {}
            if type(data) == type(tuple()):
                for i in range(0,len(data)):
                    tasks.update( { data[i]['end']: data[i]['description'] })
            else:
                tasks.update( { data['end']: data['description'] })
            
            body =  "Informe diario\n"
            body += "==============\n"
            num = 0
            for key in sorted( tasks ):
                num += 1
                body += ' {0}.- {1}\n'.format(num,tasks[key])
                
            print body
        else:
            print r.std_err