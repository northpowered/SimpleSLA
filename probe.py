from netmiko import ConnectHandler,NetmikoTimeoutException, NetmikoAuthenticationException
import textfsm
connection =  {
            'device_type': 'eltex',
            'host': '15.255.71.1',
            'username': 'romanov',
            'password': 'Pwd12345678',
            'port': 22,
        }

with ConnectHandler(**connection) as hnd:
    
    response = hnd.send_command('ping 15.255.71.2 detailed packets 1')
    print(response)
    with open('templates/eltex.template') as tmp:
        fsm = textfsm.TextFSM(tmp)
        output = fsm.ParseText(response)
        print(output[0][0])