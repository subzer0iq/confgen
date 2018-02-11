import sys
import jinja2
import netaddr

if len(sys.argv) == 1:
        print('''{0} <model> <hostname> <ipaddress/prefix> <gateway> "<location>"
        supported models:
        EX4300
        WS-C3560-48TS: Fa0/1-48 Gi0/1-4
        WS-C3560G-24TS: Gi0/1-28
        WS-C3560G-48TS: Gi0/1-53
        WS-C2950G-24-EI: Fa0/1-24 Gi0/1-2
        WS-C3750G-24TS-1U: Gi1/0/1-28
        WS-C3750-24TS: Fa1/0/24 Gi1/0/1-2
        WS-C3750E-24TD: Gi1/0/1-24 Te1/0/1-2
        '''.format(sys.argv[0]))
        sys.exit(0)
if sys.argv[1].startswith('WS-'):
        TEMPLATE_FILE_VAR = 'CISCO'
else:
        TEMPLATE_FILE_VAR = 'JUNIPER'

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)

TEMPLATE_FILE = "templates/{0}.conf".format(TEMPLATE_FILE_VAR)
template = templateEnv.get_template(TEMPLATE_FILE)

config_dict = {
    'EX4300': {
        'downlinks': ['ge-0/0/{0}'.format(i) for i in range(0, 48)],
        'uplinks': ['ge-0/2/0', 'xe-0/2/0', 'ge-0/2/1', 'xe-0/2/1', 'ge-0/2/2', 'xe-0/2/2', 'ge-0/2/3', 'xe-0/2/3']
    },
    'WS-C3560-48TS': {
        'downlinks': ['FastEthernet0/{0}'.format(i) for i in range(1, 49)],
        'uplinks': ['GigabitEthernet0/{0}'.format(i) for i in range(1, 5)]
    },
    'WS-C3560G-24TS': {
        'downlinks': ['GigabitEthernet0/{0}'.format(i) for i in range(1, 26)],
        'uplinks': ['GigabitEthernet0/{0}'.format(i) for i in range(25, 29)]
    },
    'WS-C3560G-48TS': {
        'downlinks': ['GigabitEthernet0/{0}'.format(i) for i in range(1, 49)],
        'uplinks': ['GigabitEthernet0/{0}'.format(i) for i in range(49, 53)]
    },
    'WS-C2950G-24-EI': {
        'downlinks': ['FastEthernet0/{0}'.format(i) for i in range(1, 25)],
        'uplinks': ['GigabitEthernet0/{0}'.format(i) for i in range(1, 3)]
    },
    'WS-C3750G-24TS-1U': {
        'downlinks': ['GigabitEthernet1/0/{0}'.format(i) for i in range(1, 25)],
        'uplinks': ['GigabitEthernet1/0/{0}'.format(i) for i in range(25, 29)]
    },
    'WS-C3750-24TS': {
        'downlinks': ['FastEthernet1/0/{0}'.format(i) for i in range(1, 25)],
        'uplinks': ['GigabitEthernet1/0/{0}'.format(i) for i in range(1, 3)]
    },
    'WS-C3750E-24TD': {
        'downlinks': ['GigabitEthernet1/0/{0}'.format(i) for i in range(1, 25)],
        'uplinks': ['TenGigabitEthernet1/0/{0}'.format(i) for i in range(1, 3)]
    }
}

ip = netaddr.IPNetwork(sys.argv[3])

config_vars = {
    'hostname': sys.argv[2],
    'device_location': sys.argv[5],
    'dcname': sys.argv[2].split('.')[1],
    'downlinks': config_dict[sys.argv[1]]['downlinks'],
    'uplinks': config_dict[sys.argv[1]]['uplinks'],
    'mgmt_ip_address': ip.ip.__str__(),
    'mgmt_ip_prefix': ip.prefixlen.__str__(),
    'mgmt_ip_gateway': sys.argv[4],
    'mgmt_ip_net': ip.network.__str__(),
    'mgmt_ip_netmask': ip.netmask.__str__(),
    'mgmt_ip_woldcard': ip.hostmask.__str__()
}

outputText = template.render(config_vars)
print(outputText)
