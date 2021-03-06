from cmath import log
from sla.sla import Sla
import sys
import argparse
import os
if __name__ == '__main__':

   __version__ = '1.0.1'
   __author__ = 'Romanov'

   ap = argparse.ArgumentParser()

   ap.add_argument('-c', '--config', required=True,
      help='Path to configuration yaml file')

   ap.add_argument('-v', '--verbose', required=False,
      help='Logging level',choices=['DEBUG','INFO','WARNING','ERROR'])

   ap.add_argument('-l', '--log-dest', required=False,
      help='Logging path {stdout,FILE}')

   ap.add_argument('--version', action='version', version=__version__)

   args = vars(ap.parse_args())
   log_level = args.get('verbose')
   log_dest = args.get('log_dest')
   if not log_level:
      log_level = os.getenv('SSLA_LL', 'INFO')
   if not log_dest:
      log_dest = os.getenv('SSLA_LD', 'stdout')
   try:
      sla = Sla(
         config_file=args.get('config'),
         log_level=log_level,
         log_dest=log_dest
         )
      sla.start()
   except:
      sys.exit()




