from cmath import log
from sla.sla import Sla
import sys
import argparse
import os
if __name__ == '__main__':
   ap = argparse.ArgumentParser()

   ap.add_argument("-c", "--config", required=True,
      help="Path to configuration yaml file")
   
   ap.add_argument("-l", "--log-level", required=False,
      help="Logging level",choices=['DEBUG','INFO','WARNING','ERROR'])
   
   args = vars(ap.parse_args())
   log_level = args.get('log_level')
   if not log_level:
      log_level = os.getenv('SSLA_LL', 'INFO')
   try:
      sla = Sla(
         config_file=args.get('config'),
         log_level=log_level
         )
      sla.start()
   except:
      sys.exit()




