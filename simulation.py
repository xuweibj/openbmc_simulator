import eventlet
from eventlet import wsgi
import pecan
from pecan import rest,response
from pecan.hooks import PecanHook
import json
import string
import os,sys,getopt
import shutil
import random
import time

path = sys.path[0]
data_file = path + '/all_state'
delay_type = ''
delay_time = 0

def delay_response():
    if delay_type == 'constant':
        print "Delay time is: ", delay_time
        time.sleep( delay_time )
    elif delay_type == 'random':
        delay = random.randint(0,delay_time)
        print "Delay time is: ", delay
        time.sleep( delay ) 

class HOSTTRANSController(rest.RestController):
    @pecan.expose('json')
    def put(self, data):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'power begin\n':
                data_index = index + 1
                break 

        file_object = open(data_file_ip, 'w+')

        if data == 'xyz.openbmc_project.State.Host.Transition.Off':
            lines[data_index] = 'xyz.openbmc_project.State.Host.HostState.Off' + '\n'
            lines[data_index+1] = 'xyz.openbmc_project.State.Host.Transition.Off' + '\n'
        else :
            lines[data_index] = 'xyz.openbmc_project.State.Host.HostState.Running' + '\n'
            lines[data_index+1] = 'xyz.openbmc_project.State.Host.Transition.On' + '\n'

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class ATTRController(rest.RestController):
    RequestedHostTransition = HOSTTRANSController()

class HOST0Controller(rest.RestController):
    @pecan.expose('json')
    def get(self):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'power begin\n':
                text = lines[index+1].strip()
                trans = lines[index+2].strip()
                break

        status_data = {"CurrentHostState" : text, "RequestedHostTransition" : trans}
        out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}

        delay_response()
        return out_data

    attr = ATTRController()

class STATEController(rest.RestController):
    host0 = HOST0Controller()

class BOOTController(rest.RestController):
    @pecan.expose('json')
    def put(self, data):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'boot begin\n':
                data_index = index + 1
                break

        file_object = open(data_file_ip, 'w+')

        lines[data_index] = data + '\n'

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

    @pecan.expose('json')
    def get(self):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'boot begin\n':
                text = lines[index +1].strip() 
                break

        status_data = {"BootSource" : text}
        out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}
        delay_response()
        return out_data 

class IPV4Controller(rest.RestController):
    @pecan.expose('json')
    def get_data(self):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'network begin\n':
                ip_addr = lines[index+2].strip()
                netmask = lines[index+4].strip()
                gateway = lines[index+6].strip()
                vlan = lines[index+8].strip()
            if lines[index] == 'network end\n':
                break

        status_data = {"Address" : ip_addr, "Gateway" : gateway, 
                       "Netmask" : netmask, "VLAN" : vlan,
                       "origin" : "xyz.openbmc_project.Network.IP.AddressOrigin.Static", 
                       "PrefixLength" : 24, "Type" : "xyz.openbmc_project.Network.IP.Protocol.IPv4"}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

class IPV4BController(rest.RestController):
    @pecan.expose('json')
    def get_data(self):
        status_data = {"Address" : "9.3.23.30", "Gateway" : "0.0.0.0",
                       "Netmask" : "255.255.255.0", "VLAN" : "9.3.23.30",
                       "origin" : "xyz.openbmc_project.Network.IP.AddressOrigin.Static",
                       "PrefixLength" : 23, "Type" : "xyz.openbmc_project.Network.IP.Protocol.IPv4"}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

class INTERFACEController(rest.RestController):
    @pecan.expose('json')
    def get_data(self):
        status_data = {"AutoNeg" : 0, "DHCPEnabled" : 0,
                       "DomainName" : [], "InterfaceName" : "eth0",
                       "MACAddress" : "70:E2:84:14:28:76", "Nameservers" : []}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

class NETWORKController(rest.RestController):
    @pecan.expose('json')
    def put(self, data):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        file_object = open(data_file_ip, 'r+')

        dict_net = {}
        data_list = data.split(',')
        for string in data_list:
            info = string.split(': ')
            key = info[0]
            dict_net[key] = info[1]

        try:
            lines = file_object.readlines()
        finally:
            file_object.close()

        for index in range(len(lines)):
            if lines[index] == 'ip\n':
                if dict_net.has_key('ip'):
                    lines[index+1] = dict_net['ip'] + '\n'
            if lines[index] == 'netmask\n':
                if dict_net.has_key('netmask'):
                    lines[index+1] = dict_net['netmask'] + '\n'
            if lines[index] == 'gateway\n':
                if dict_net.has_key('gateway'):
                    lines[index+1] = dict_net['gateway'] + '\n'
            if lines[index] == 'vlan\n':
                if dict_net.has_key('vlan'):
                    lines[index+1] = dict_net['vlan'] + '\n'

        file_object = open(data_file_ip, 'w+')

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            interface_data = INTERFACEController().get_data()
            ipv4_data1 = IPV4Controller().get_data()
            ipv4_data2 = IPV4BController().get_data()

        status_data = {"/xyz/openbmc_project/network/eth0" : interface_data, 
                       "/xyz/openbmc_project/network/eth0/ipv4/31f4ce8b" : ipv4_data1,
                       "/xyz/openbmc_project/network/eth0/ipv4/e9767624" : ipv4_data2} 
        out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}
        delay_response()
        return out_data

    ipv4 = IPV4Controller()

class MTRBRDController(rest.RestController):
    def get_data(self):
        status_data = {'Model' : 'SIMULATER', 'PartNumber' : '00VK525', 'SerialNumber' : 'Y130UF72701M'}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data    

class DIMMController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        status_data = {'PartNumber' : '', 'SerialNumber' : '0x15d27a18' , 'Model' : '36ASF4G72PZ-2G6D1' , 'Version' : '0x31' , 'Manufacturer' : '0x2c80'}
        return status_data

class CPUController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        status_data = {'SerialNumber' : 'YA3933800321' , 'PrettyName' : 'PROCESSOR MODULE' , 'PartNumber' : '01HL966' , 'Version' : '10' , 'Manufacturer' : 'IBM'}
        return status_data

class COREController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        status_data = {'PrettyName' : '', 'Functional' : '1' , 'Present' : '1'}
        return status_data

class CHASSISController(rest.RestController):
    motherboard = MTRBRDController()

class SYSTEMController(rest.RestController):
    @pecan.expose('json')
    def get_data(self):
        status_data = {'SerialNumber' : '0000000000000000', 'Model' : '2', 'PartNumber' : '0000000000000000' , 'PrettyName' : '', 'Manufacturer' : ''}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    chassis = CHASSISController()

class DEVICEController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        status_data = {'deviceid' : '0x01', 'guiduuid' : '0x0001', 'mprom' : '1024'}
        return status_data

class INVENTORYController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            mtrbrd_data = MTRBRDController().get_data()
            dimm_data = DIMMController().get()
            cpu_data = CPUController().get()
            core_data = COREController().get() 
            system_data = SYSTEMController().get()
            device_data = DEVICEController().get()
            all_data = {'/xyz/openbmc_project/inventory/system/chassis/motherboard' : mtrbrd_data, 
                '/xyz/openbmc_project/inventory/system/chassis/motherboard/dimm1' : dimm_data, 
                '/xyz/openbmc_project/inventory/system/chassis/motherboard/cpu1' : cpu_data, 
                '/xyz/openbmc_project/inventory/system/chassis/motherboard/cpu0/core1' : core_data, 
                '/xyz/openbmc_project/inventory/system' : system_data, 
                '/xyz/openbmc_project/inventory/system/device' : device_data}
            out_data = {"status" : "ok", "data" : all_data, "message" : "200 OK"}
            delay_response()
            return out_data

    system = SYSTEMController()

class FIRMController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        data = {'Activation' : 'xyz.openbmc_project.Software.Activation.Activations.Active',
            'Purpose' : 'xyz.openbmc_project.Software.Version.VersionPurpose.BMC',
             'RequestedActivation' : 'xyz.openbmc_project.Software.Activation.RequestedActivations.None',
            'Version' : 'v1.99.5-20-gabef2cb'}
        url_data = {'/xyz/openbmc_project/software/b5310f74' : data}
        return url_data

class SOFTWAREController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            firm_data = FIRMController().get()
            out_data = {"status" : "ok", "data" : firm_data, "message" : "200 OK"}
            delay_response()
            return out_data

class FANController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        data = {'Value' : 7668,
                'Target' : 0,
                'Unit' : 'xyz.openbmc_project.Sensor.Value.Unit.RPMS',
                'Scale' : 0}
        return data

class PCIEController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        data = {'Value' : 30312,
                'Unit' : 'xyz.openbmc_project.Sensor.Value.Unit.DegreesC',
                'Scale' : -3}
        return data

class SENSORSController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            fan_data = FANController().get()
            pcie_data = PCIEController().get()
            all_data = {'/xyz/openbmc_project/sensors/fan_tach/fan0' : fan_data,
                        '/xyz/openbmc_project/sensors/temperature/pcie' :  pcie_data} 
            out_data = {"status" : "ok", "data" : all_data, "message" : "200 OK"}
            delay_response()
            return out_data


class CLEARController(rest.RestController):
    @pecan.expose('json')
    def post(self, data):
        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class ACTIONController(rest.RestController):
    clear = CLEARController()

class ENTRYController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        entry_1 = {'Timestamp' : '1494489410865', 'Id' : '1',
            'Message' : 'org.open_power.Error.Host.Event.Event',
            'Severity' : 'xyz.openbmc_project.Logging.Entry.Level.Informational'} 
        entry_2 = {'Timestamp' : '1494557035998', 'Id' : '2',
            'Message' : 'org.open_power.Error.Host.Event.Event',
            'Severity' : 'xyz.openbmc_project.Logging.Entry.Level.Informational'}
        entry_data = {'1' : entry_1, '2' : entry_2}
        return entry_data

class LOGGINGController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            entry_data = ENTRYController().get()
            out_data = {"status" : "ok", "data" : entry_data, "message" : "200 OK"}
            delay_response()
            return out_data

    action = ACTIONController()

class OPENBMCController(rest.RestController):
    state = STATEController()
    boot = BOOTController()
    network = NETWORKController()
    inventory = INVENTORYController()
    software = SOFTWAREController()
    logging = LOGGINGController()
    sensors = SENSORSController()

class XYZController(rest.RestController): 
    openbmc_project = OPENBMCController()

class LOGINController(rest.RestController):
    @pecan.expose('json')
    def post(self, data):
        if data == ["root", "0penBmc"]:
            out_data = {"status" : "ok", "message" : "200 OK"}
        else:
            description = "Invalid username or password"
            out_data = {"status" : "error", "data" : {"description" : description}, "message" : "401 Unauthorized"}
            pecan.response.status = 401
        return out_data

class Root(object):
    xyz = XYZController()
    login = LOGINController()

config = {
    'root': Root,
    'debug': True,
}
 
def _make_app():
    app = pecan.make_app(**config)
    return app
 
def main(argv):
    global delay_time, delay_type
    try:
        opts, args = getopt.getopt(argv, "d:t:")
    except getopt.GetoptError:
        print 'Error'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            delay_type = arg
        elif opt == '-t':
            delay_time = arg

    delay_time = int(delay_time)
    if (delay_type):
        if (delay_type != 'constant') and (delay_type != 'random'):
            print "Only constant and random are supported"
            sys.exit (1)

    os.system('nc -l 2200 &')
    eventlet.monkey_patch()
    app = _make_app()
    port = 443 
    wsgi.server(eventlet.wrap_ssl(eventlet.listen(('',port)), certfile=path + '/server.cert',
                                  keyfile=path + '/server.key', server_side=False), app)
 
if __name__ == '__main__':
    main(sys.argv[1:])
