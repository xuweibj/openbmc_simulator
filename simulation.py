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

#-------------------- SIMULATOR FOR RPOWER --------------------#

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
            if lines[index] == 'host begin\n':
                data_index = index + 1
            if lines[index] == 'chassis begin\n':
                chassis_index = index + 1

        file_object = open(data_file_ip, 'w+')

        if data == 'xyz.openbmc_project.State.Host.Transition.Off':
            lines[data_index] = 'xyz.openbmc_project.State.Host.HostState.Off' + '\n'
            lines[data_index+1] = 'xyz.openbmc_project.State.Host.Transition.Off' + '\n'
            lines[chassis_index] = 'xyz.openbmc_project.State.Chassis.PowerState.Off' + '\n'
            lines[chassis_index+1] = 'xyz.openbmc_project.State.Chassis.Transition.Off' + '\n'
        else :
            lines[data_index] = 'xyz.openbmc_project.State.Host.HostState.Running' + '\n'
            lines[data_index+1] = 'xyz.openbmc_project.State.Host.Transition.On' + '\n'
            lines[chassis_index] = 'xyz.openbmc_project.State.Chassis.PowerState.On' + '\n'
            lines[chassis_index+1] = 'xyz.openbmc_project.State.Chassis.Transition.Off' + '\n'

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class BMCTRANSController(rest.RestController):
    @pecan.expose('json')
    def put(self, data):
        req_ip = pecan.request.server_name
        data_file_ip = data_file + '_' + req_ip

        if not os.path.exists(data_file_ip):
            shutil.copy(data_file, data_file_ip)

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class POWERTRANSController(rest.RestController):
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
            if lines[index] == 'chassis begin\n':
                chassis_index = index + 1
                break

        file_object = open(data_file_ip, 'w+')

        if data == 'xyz.openbmc_project.State.Chassis.Transition.Off':
            lines[chassis_index] = 'xyz.openbmc_project.State.Chassis.PowerState.Off' + '\n'
            lines[chassis_index+1] = 'xyz.openbmc_project.State.Chassis.Transition.Off' + '\n'

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()
        
        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class ATTRController(rest.RestController):
    RequestedHostTransition = HOSTTRANSController()
    RequestedBMCTransition = BMCTRANSController()
    RequestedPowerTransition = POWERTRANSController()

class BMC0Controller(rest.RestController):
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
            if lines[index] == 'bmc begin\n':
                text = lines[index+1].strip()
                trans = lines[index+2].strip()
                break

        status_data = {"CurrentBMCState" : text, "RequestedBMCTransition" : trans}

        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    attr = ATTRController()

class CHASSIS0Controller(rest.RestController):
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
            if lines[index] == 'chassis begin\n':
                text = lines[index+1].strip()
                trans = lines[index+2].strip()
                break

        status_data = {"CurrentPowerState" : text, "RequestedPowerTransition" : trans}

        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    attr = ATTRController()

class HOST0Controller(rest.RestController):
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
            if lines[index] == 'host begin\n':
                text = lines[index+1].strip()
                trans = lines[index+2].strip()
                break

        status_data = {"CurrentHostState" : text, "RequestedHostTransition" : trans}

        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    attr = ATTRController()

class ALLSTATEController(rest.RestController):
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
            if lines[index] == 'host begin\n':
                host_text = lines[index+1].strip()
                host_trans = lines[index+2].strip()
            if lines[index] == 'bmc begin\n':
                bmc_text = lines[index+1].strip()
                bmc_trans = lines[index+2].strip()
            if lines[index] == 'chassis begin\n':
                chassis_text = lines[index+1].strip()
                chassis_trans = lines[index+2].strip()

        chassis_state = {"CurrentPowerState" : chassis_text, "RequestedPowerTransition" : chassis_trans}
        bmc_state = {"CurrentBMCState" : bmc_text, "RequestedBMCTransition" : bmc_trans}
        host_state = {"CurrentHostState" : host_text, "RequestedHostTransition" : host_trans} 
        status_data = {"/xyz/openbmc_project/state/bmc0" : bmc_state,
                       "/xyz/openbmc_project/state/chassis0" : chassis_state,
                       "/xyz/openbmc_project/state/host0" : host_state}
        return status_data

class STATEController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            status_data = ALLSTATEController().get_data()

            out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}
            delay_response()
            return out_data 


    bmc0 = BMC0Controller()
    chassis0 = CHASSIS0Controller()
    host0 = HOST0Controller()

#-------------------- SIMULATOR FOR RINV --------------------#

class MTRBRDController(rest.RestController):
    def get_data(self):
        status_data = {'Model' : 'SIMULATER', 'PartNumber' : '00VK525', 'SerialNumber' : 'Y130UF72701M', 'Present' : 1}
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
        status_data = {'PartNumber' : '', 'SerialNumber' : '0x15d27a18' , 'Model' : '36ASF4G72PZ-2G6D1' , 'Version' : '0x31' , 'Manufacturer' : '0x2c80', 'Present' : 1}
        return status_data

class CPUController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        status_data = {'SerialNumber' : 'YA3933800321' , 'PrettyName' : 'PROCESSOR MODULE' , 'PartNumber' : '01HL966' , 'Version' : '10' , 'Manufacturer' : 'IBM', 'Present' : 1}
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
        req_ip = pecan.request.server_name
        serial = req_ip.replace('.','')
        status_data = {'SerialNumber' : serial, 'Model' : 'OPENBMC', 'PartNumber' : 'SIMULATOR', 'PrettyName' : '', 'Manufacturer' : '', 'Present' : 1}
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
        status_data = {'deviceid' : '0x01', 'guiduuid' : '0x0001', 'mprom' : '1024', 'Present' : 1}
        return status_data

class INVENTORYController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            mtrbrd_data = MTRBRDController().get_data()
            dimm_data = DIMMController().get()
            cpu_data = CPUController().get()
            core_data = COREController().get() 
            system_data = SYSTEMController().get_data()
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
        bmc_data = {"Version" :  "ibm-v1.99.10-0-r11-0-g9c65260",
                "Purpose" : "xyz.openbmc_project.Software.Version.VersionPurpose.BMC",
                "Priority" : 0,
                "Activation" : "xyz.openbmc_project.Software.Activation.Activations.Active"}
        host_data = {"Purpose" : "xyz.openbmc_project.Software.Version.VersionPurpose.Host",
                     "Activation" :  "xyz.openbmc_project.Software.Activation.Activations.Active",
                     "Version" :  "IBM-witherspoon-redbud-ibm-OP9_v1.19_1.33",
                     "Priority" : 0}
        url_data = {'/xyz/openbmc_project/software/9e55358e' : bmc_data,
                    '/xyz/openbmc_project/software/221d9020' : host_data}
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

#-------------------- SIMULATOR FOR REVENTLOG --------------------#

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

#-------------------- SIMULATOR FOR RBEACON --------------------#

class BEACONASSController(rest.RestController):
    @pecan.expose('json')
    def put(self, data):
        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class BEACONController(rest.RestController):
    Asserted = BEACONASSController()

class ENIDController(rest.RestController):
    attr = BEACONController()

class GRPController(rest.RestController):
    enclosure_identify = ENIDController()

class LEDController(rest.RestController):
    groups = GRPController()

#-------------------- SIMULATOR FOR RSETBOOT --------------------#

class BOOTONESRCController(rest.RestController):
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
            if lines[index] == 'boot one time begin\n':
                data_index = index + 2
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

class BOOTONEENBController(rest.RestController):
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
            if lines[index] == 'boot one time begin\n':
                data_index = index + 1
                break

        file_object = open(data_file_ip, 'w+')

        lines[data_index] = str( data ) + '\n'

        try:
            file_object.writelines(lines)
        finally:
            file_object.close()

        out_data = {"status" : "ok", "message" : "200 OK"}
        delay_response()
        return out_data

class BOOTONEATTRController(rest.RestController):
    BootSource = BOOTONESRCController()
    Enabled = BOOTONEENBController()

class BOOTONEController(rest.RestController):
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
            if lines[index] == 'boot one time begin\n':
                enabled = lines[index +1].strip()
                source  = lines[index +2].strip()
                break

        status_data = {"Enabled": enabled, "BootSource" : source}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    attr = BOOTONEATTRController()

class BOOTSRCController(rest.RestController):
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

class BOOTATTRController(rest.RestController):
    BootSource = BOOTSRCController()

class BOOTController(rest.RestController):
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
            if lines[index] == 'boot begin\n':
                text = lines[index +1].strip()
                break

        status_data = {"BootSource" : text}
        return status_data

    @pecan.expose('json')
    def get(self):
        data = self.get_data()
        out_data = {"status" : "ok", "data" : data, "message" : "200 OK"}
        delay_response()
        return out_data

    attr = BOOTATTRController()
    one_time = BOOTONEController()

class CNLHOST0Controller(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            boot_status = BOOTController().get_data()
            boot_one_time = BOOTONEController().get_data()
            status_data = {"/xyz/openbmc_project/control/host0/boot/one_time" : boot_one_time,
                           "/xyz/openbmc_project/control/host0/boot" : boot_status}
            out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}
            delay_response()
            return out_data

    boot = BOOTController()

class CONTROLController(rest.RestController):
    host0 = CNLHOST0Controller()

#-------------------- SIMULATOR FOR RSPCONFIG --------------------#

class NETWORKController(rest.RestController):
    @pecan.expose('json')
    def get(self, arg):
        if arg == 'enumerate':
            req_ip = pecan.request.server_name
            eth0_object = {"InterfaceName" : "eth0", "DHCPEnabled" : "0", "MACAddress" : "70:e2:84:14:28:d"}
            ip_object = {"Type" : "xyz.openbmc_project.Network.IP.Protocol.IPv4", "Address" : req_ip, "PrefixLength" : 8, "Gateway" : "0.0.0.0"}
            config_object = {"DefaultGateway" : "", "HostName" : "witherspoon"}
            dhcp_object = {"DNSEnabled" : 1, "NTPEnabled" : 1, "HostNameEnabled" : 1}

            status_data = {"/xyz/openbmc_project/network/eth0" : eth0_object,
                           "/xyz/openbmc_project/network/config/dhcp" : dhcp_object,
                           "/xyz/openbmc_project/network/eth0/ipv4/111111" : ip_object,
                           "/xyz/openbmc_project/network/config" : config_object}

            out_data = {"status" : "ok", "data" : status_data, "message" : "200 OK"}
            delay_response()
            return out_data


#--------------------------------------------
# PROJECT CONTROLLER
#--------------------------------------------
class OPENBMCController(rest.RestController):
    state = STATEController()
    inventory = INVENTORYController()
    software = SOFTWAREController()
    logging = LOGGINGController()
    sensors = SENSORSController()
    led = LEDController()
    control = CONTROLController()
    network = NETWORKController()

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

    eventlet.monkey_patch()
    app = _make_app()
    port = 443 
    wsgi.server(eventlet.wrap_ssl(eventlet.listen(('',port)), certfile=path + '/server.cert',
                                  keyfile=path + '/server.key', server_side=False), app)
 
if __name__ == '__main__':
    main(sys.argv[1:])
