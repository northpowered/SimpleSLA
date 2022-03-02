from netmiko import ConnectHandler,NetmikoTimeoutException, NetmikoAuthenticationException
import textfsm
from sla.logger import LG
from ping3 import ping
from sla.tracer import device_tracer, rtt_tracer

class Device():
    def __init__(self, **parameters) -> None:
        self.name = parameters['name']
        self.type = parameters['type']
        self.transport = parameters.get('transport',None)
        self.address = parameters.get('address',None)
        self.username = parameters.get('username',None)
        self.password = parameters.get('password',None)
        self.port = parameters.get('port')
        self.template = parameters.get('template',None)

        
    def __get_rtt_remote(self, target:str):
        connection =  {
            'device_type': 'generic',
            'host': self.address,
            'username': self.username,
            'password': self.password,
            'port': self.port,
        }
        command = str()
        template = str()
        #Selecting connection args in case of device type
        if self.type == 'm716':
            command = f"ping -c 1 {target}"
            if self.transport == 'ssh':
                connection['device_type'] = 'generic'
            else:
                LG.error(f"Unsupported transport {self.transport} for m716 device type")
                return None
        elif self.type == 'cisco':
            command = f"ping {target} repeat 1"
            if self.transport == 'telnet':
                connection['device_type'] = 'cisco_ios_telnet'
            elif self.transport == 'ssh':
                pass #ssh cisco
            else:
                LG.error(f"Unsupported transport {self.transport} for cisco device type")
                return None
        else:
            return None
        try:
            _= None
            with ConnectHandler(**connection) as hnd:
                LG.debug(f"Connected to {self.name} device")
                result = hnd.send_command(command)
                LG.debug(f"RTT command sent to {self.name} device")
                fsm = textfsm.TextFSM(self.template)
                output = fsm.ParseText(result)
                try:
                    _ = float(output[0][0])
                except IndexError:
                    _ = None
                except:
                    _ = False
                finally:
                    return _
        except FileNotFoundError:
            LG.error(f"Template file {template} not found")
        except NetmikoTimeoutException:
            LG.warning(f"Unreachable device. Connection with {self.name} failed")
        except NetmikoAuthenticationException as error:
            LG.warning(f"Authentication with {self.name} failed. Check credentials")
        else:
            pass
        finally:
            return _

    def __get_rtt_local(self, target:str):
        _ = None
        try:
            _ = ping(
                target,
                timeout=1,
                unit='ms',
                src_addr='0.0.0.0',
                ttl=64, 
                size=56
                )
        except UnicodeError:
            LG.error(f"Wrong Ipv4 syntax: {target}")
        except OSError as error:
            LG.error(f"Source interface/address {error} is not exist")
        else:
            pass
        finally:
            return _

    def get_rtt(self, target:str):
        with device_tracer.start_as_current_span(__name__) as span:
            span.set_attribute("device.type", self.type)
            span.set_attribute("device.target", target) 
            rtt = int()
            if self.type in ['m716','cisco']:
                rtt = self.__get_rtt_remote(target)
            elif self.type == 'local':
                rtt = self.__get_rtt_local(target)
            else:
                LG.error(f"Unknown device type >> {self.type} << ")
            if rtt is not None:
                span.set_attribute("device.rtt", rtt)
            return rtt