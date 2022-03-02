import yaml
from sla.service import Service
from sla.device import Device
from sla.policy import Policy
from sla.logger import LG

AVAILABLE_SERVICE_TYPES = ['simple-check','device']
class SLAConfig():

    def __init__(self,config_file:str) -> None:
        LG.info(f"Using config file {config_file}")
        self.config_file = config_file      
        self._config = self._load_config(self._load_file())
        LG.info("Configuration loaded")

        


    def _load_file(self):
        result = {
            'error':None,
            'data':None
        }
        with open(self.config_file,'r') as f:
            config = yaml.safe_load(f)
            result['data'] = config
            LG.info(f"File {self.config_file} was loaded successfuly")
        
        return result

    def _load_config(self,config_from_file):
        
        parsed_configuration = {
            'server':{
                'bind_address': '127.0.0.1',
                'port':8800,
                'refresh_time': 1,
            },
            'global':{
                'unit': 'ms',
            },
            'local': dict(),
            'devices': dict(),
            'services': dict(),
            'policies': dict(),
        }


        if config_from_file.get('error',''):
            self.LG.error("conf read error #REDONE")

        config_data = config_from_file.get('data')


        parsed_configuration['server']['bind_address'] = config_data.get('server').get('bind_address','127.0.0.1')
        parsed_configuration['server']['port'] = config_data.get('server').get('port','8800')
        parsed_configuration['server']['refresh_time'] = config_data.get('server').get('refresh_time','1')

        #Creating devices
        for raw_device in config_data.get('devices',list()):
            device = dict()
            
            #Parsing name field in device object
            try:
                device['name'] = raw_device['name']
            except KeyError:
                LG.error("Cannot find device NAME")
            else:
                if not isinstance(device['name'],str):
                    LG.error("Device name >> {name} << should be String type",name=device['name'])
            
            #Parsing type field in device object
            try:
                device['type'] = raw_device['type']
            except KeyError:
                LG.error("Cannot find TYPE of {name} device",name = device['name'])
            else:
                if not isinstance(device['type'],str):
                    LG.error("Device type >> {type} << should be String type",type=device['type'])

            #Appending template to device

            with open(f"templates/{device['type']}.template") as template:
                device['template'] = template

            #Parsing transport field in device object
            try:
                device['transport'] = raw_device['transport']
            except KeyError:
                LG.error("Cannot find TRANSPORT of {name} device",name = device['name'])
            else:
                if not isinstance(device['transport'],str):
                    LG.error("Device transport >> {transport} << should be String type",transport=device['transport'])

            #Parsing address field in device object
            try:
                device['address'] = raw_device['address']
            except KeyError:
                LG.error("Cannot find ADDRESS of {name} device",name = device['name'])
            else:
                if not isinstance(device['address'],str):
                    LG.error("Device address >> {address} << should be String type",address=device['address'])

            #Parsing username field in device object
            try:
                device['username'] = raw_device['username']
            except KeyError:
                LG.error("Cannot find USERNAME of {name} device",name = device['name'])
            else:
                if not isinstance(device['username'],str):
                    LG.error("Device username >> {username} << should be String type",username=device['username'])

            #Parsing password field in device object
            try:
                device['password'] = raw_device['password']
            except KeyError:
                LG.error("Cannot find PASSWORD of {name} device",name = device['name'])
            else:
                if not isinstance(device['password'],str):
                    LG.error("Device password >> {password} << should be String type",password=device['password'])
                      
            #Parsing port field in device object
            try:
                device['port'] = raw_device['port']
            except KeyError:
                LG.error("Cannot find PORT of {name} device",name = device['name'])
            else:
                if not isinstance(device['port'],int):
                    LG.error("Device port >> {port} << should be Int type",port=device['port'])
            #Appendind Device object with parsed params to configuration
            parsed_configuration['devices'][device['name']] = Device(**device)
            #Creating local permanent device
            local_device = {
                'name':'simplesla-local',
                'type':'local',
            }
            #Appending local device 
            parsed_configuration['devices'][local_device['name']] = Device(**local_device)

        #Creating policies
        for raw_policy in config_data.get('policies',list()):
            policy = dict()
            
            #Parsing name field in policy object
            try:
                policy['name'] = raw_policy['name']
            except KeyError:
                LG.error("Cannot find policy NAME")
            else:
                if not isinstance(policy['name'],str):
                    LG.error("Policy name >> {name} << should be String type",name=policy['name'])
            
            #Parsing max_rtt field in policy object
            try:
                policy['max_rtt'] = raw_policy['max_rtt']
            except KeyError:
                LG.error("Cannot find policy MAX_RTT")
            else:
                if not isinstance(policy['max_rtt'],(int, float)):
                    LG.error("Policy max_rtt >> {max_rtt} << should be Int or Float type",max_rtt=policy['max_rtt'])

            #Appending policy to configuration
            parsed_configuration['policies'][policy['name']] = Policy(
                name=policy['name'],
                max_rtt=policy['max_rtt'],
            )
        #Creating services
        for raw_service in config_data.get('services',list()):
            service  = dict()
            #Parsing name field in service object
            try:
                service['name'] = raw_service['name']
            except KeyError:
                LG.error("Cannot find service NAME")
            else:
                if not isinstance(service['name'],str):
                    LG.error("Service name >> {name} << should be String type",name=service['name'])
            #Parsing device field in service object
            try:
                _ = raw_service['device']
            except KeyError:
                LG.error("Cannot find DEVICE of {name} service",name = service['name'])
            else:
                if not isinstance(_,str):
                    LG.error("Service device >> {device} << should be String type",device=_)
                try:
                    service['device'] = parsed_configuration['devices'][_]
                except KeyError:
                    LG.error("Unknown device {device} in {service} service",device = _, service = service['name'])


            #Parsing device field in service object
            try:
                service['target'] = raw_service['target']
            except KeyError:
                LG.error("Cannot find TARGET of {name} service",name = service['name'])
            else:
                if not isinstance(service['target'],str):
                    LG.error("Service target >> {target} << should be String type",target=service['target'])
            
            
            #Parsing policy field in service object
            try:
                _ = raw_service['policy']
            except KeyError:
                service['policy'] = None
            else:
                if not isinstance(_,str):
                    LG.error("Service policy >> {policy} << should be String type",policy=_)
                try:
                    service['policy'] = parsed_configuration['policies'][_]
                except KeyError:
                    LG.error("Unknown policy {policy} in {service} service",policy = _, service = service['name'])
            

            #Parsing delay field in service object
            try:
                service['delay'] = raw_service['delay']
            except KeyError:
                LG.error("Cannot find DELAY of {name} service",name = service['name'])
            else:
                if not isinstance(service['delay'],int):
                    LG.error("Service delay >> {delay} << should be Int type",type=service['delay'])
                
            #Appendind Service object with parsed params to configuration
            parsed_configuration['services'][service['name']] = Service(
                name=service['name'],
                device=service['device'],
                target=service['target'],
                delay=service['delay'],
                description='temp descrp',
                verbose_name='temp_verb',
                policy=service['policy'],
            )
            
        return parsed_configuration
        
    def getServices(self):
        return self._config.get('services',dict())

    def getBindAddress(self):
        return self._config['server']['bind_address']

    def getBindPort(self):
        return self._config['server']['port']
    
    def getRefreshTime(self):
        return self._config['server']['refresh_time']