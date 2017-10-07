import argparse
import sys
import re
sys.path.append("/home/efim/Dropbox")
from  ipcalc_flask import calculateSubnet as calc
import dcim_s_r
from json_p_n import sendRecieve as sr
class AddServer:

    '''This class should add a server to DCIM'''

    def __init__(self,subnet = None,serverName = None,serverTypeId = None, hostname = None, ipmiUser = None, ipmiPassword = None, vlan = None):
        self.subnet = subnet
        self.cidr = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$'
        self.sevenThFloor ='^(710[AB])[0-9]{1,2}R[0-9]{1,2}.'
        self.serverName = serverName
        self.plid =""
        self.mac = ""
        self.ipmiIp = ""
        self.switchIP = ""
        self.switchPort = ""
        self.serverTypeId = serverTypeId
        #self.serverChassisTempl = ""
        self.serverRackId = ""
        self.hostname = hostname
        self.ipmiPassword = ipmiPassword
        self.ipmiUser = ipmiUser
        self.vlan = vlan
        self.switchId = ""
        self.portId = ""
    
    def add_subnet(self):
        ''' This method will add subnet to DCIM'''
        if re.match(self.cidr,self.subnet):             
            
            print (dcim_s_r.sendRecieveDCIM("ipdb.edit",{"range": self.subnet, "netmask": calc(self.subnet)[3], "gateway": calc(self.subnet)[1], "sok": "ok"}))
         
        
        else:
            print("You didn't enter the propper CIDR")
            exit()    
    def add_server(self):
        #pass
        if self.serverName[-2:-1].isalpha():
            unit = self.serverName[-1:]
        else:
            unit =  self.serverName[-2:]   
        #blade_slot=&chassis_ram=&chassistempl=2&clicked_button=ok&cpu_0=null&cpu_count=1&family=ipv4&forcelock=off&func=server.edit&hdd_0=null&hdd_1=null&hdd_10=null&hdd_11=null&hdd_12=null&hdd_13=null&hdd_14=null&hdd_15=null&hdd_16=null&hdd_17=null&hdd_18=null&hdd_19=null&hdd_2=null&hdd_20=null&hdd_21=null&hdd_22=null&hdd_23=null&hdd_24=null&hdd_25=null&hdd_26=null&hdd_27=null&hdd_28=null&hdd_29=null&hdd_3=null&hdd_4=null&hdd_5=null&hdd_6=null&hdd_7=null&hdd_8=null&hdd_9=null&hostname=free.ds&hwproblem=off&ip_block=public&is_blade2=&is_multinode2=&mac=00%3A26%3A9E%3AB5%3AE7%3A16&name=710A14R10&notes=&operafake=1502736475316&owner=no%5Fowner&parent_chassis=no%5Fowner&pci_0=null&pci_1=null&pci_2=null&pci_3=null&pci_4=null&pci_5=null&pci_6=null&progressid=false&rack=1&sfrom=ajax&sizefromtype2=on&sok=ok&specialip=&srvsize2=&srvtypesize2=1&unit2=10'
        dcim_s_r.sendRecieveDCIM("server.edit",{"chassistempl":self.serverTypeId,"family":"ipv4","hostname": self.hostname,"mac": self.mac,"name":self.serverName,
        
        "rack":self.serverRackId, "unit":unit, "unit2":unit, "sok": "ok"})
        ''' please be careful with "self.serverName[-2:]" it does not suprt blades '''
    def add_connections(self):
        ''' This function will add a connection between the server and the switch '''
 
        switches = dcim_s_r.sendRecieveDCIM("switch",{})
        switchId = list(filter((lambda x: x if x['ip'] == self.switchIP else None),switches))[0]['id']
        ports = dcim_s_r.sendRecieveDCIM("switch.port",{"elid": switchId})
        portId = list(filter((lambda x: x if x['descr'] == self.switchPort else None),ports))[0]['id']
        dcim_s_r.sendRecieveDCIM("server.connection.connwizport", {"plid":self.plid, "port": portId, "devtype": "switch", "switch":switchId, "sok": "ok"})
        return switchId,portId
    def find_mac_and_ipmi_ip(self):
        ''' We will use NOC-PS to get the MAC and IPMI\'s IP''' 
        
        remMe = sr("searchHosts",{'start': 0, 'limit': 1000, 'query': self.serverName})['result']['data']
        if len(remMe) == 0: print('No proper server was found, exiting'); exit()
     
        ##print(remMe)
        for i in  remMe:
            ''' Actually we need the only accurate result'''
            if i['descr'].split('(')[0] == self.serverName:
                mac,ipmiIp = i['mac'],i['ipmi_ip']
        return mac, ipmiIp
    def get_the_switch_info(self):
        '''This function returns switch information where server is connected to'''

        connection = sr("getConnectionsByHost", self.mac)['result']['data']
        switchName = connection[0]['devname']
        switchPort = connection[0]['portdescr'].split(' ')[1].split('[')[1].split(']')[0]
        devices = sr("getDevices", 0, 1000)['result']['data']
        switchIP = [device['ip'] for device in devices  if device['name'] == switchName ][0] 
        if switchPort[:2] == "Gi":
            switchPort = "GigabitEthernet" + switchPort[2:]
        else:
            switchPort = "FastEthernet" + switchPort[2:]
        return switchIP, switchPort
    def print_server_types(self):
        '''This function return servers types ids and their descriptions'''
        serverTypesFull = dcim_s_r.sendRecieveDCIM("chassistempl",{})
        
        serverTypesReduced = []
        for s in serverTypesFull:
            temp=["",""]
            temp[0],temp[1] = s["id"],s["name"] 
            if temp not in serverTypesReduced:
                serverTypesReduced.append(temp)
        return serverTypesReduced
    '''
    def get_server_chassis_templ(self,serverTypesList,serverTypeId):
        for i in serverTypesList:
            if i[0] == serverTypeId:
                serverChassisTempl = i[1]
        return serverChassisTempl
    '''
    def get_plid(self):

        '''we we need it to set connections '''
        serverList = dcim_s_r.sendRecieveDCIM("server",{})
        for server in serverList:
            if server["name"] == self.serverName:
                plid = server["id"]
        return plid        
    def add_ipmi(self):
        
        
        #"clicked_button=finish&devtype=dev%5Fipmi&func=server.connection.connwizipmi&hfields=intel%5Famt&ip=68.64.173.125&ipmi=ipmi%5Flanplus&ipmipass=freefromwg40&ipmiproxy=off&ipmiuser=root&operafake=1502880698570&plid=127&progressid=false&service=off&sfrom=ajax&sok=ok&web_u
        dcim_s_r.sendRecieveDCIM("server.connection.connwizipmi",{"sok":"ok", "plid": self.plid, "ip": self.ipmiIp, "ipmi": "ipmi_lanplus", "ipmiuser": self.ipmiUser, "ipmipass" : self.ipmiPassword, "devtype" : "dev_ipmi" })
    def get_cabinet_id(self):
        racks = dcim_s_r.sendRecieveDCIM("rack",{})
        switches = dcim_s_r.sendRecieveDCIM("switch",{})
        cabinetId = list(filter((lambda x: x if x['ip'] == self.switchIP else None),switches))[0]['rack_id']
        ##FIX ME
        '''
        if re.match(self.sevenThFloor,self.serverName):
            
            cabinetName = self.serverName[0:(len(self.serverName) -3)]
        elif self.serverName[1] == '0' and  not self.serverName[2].isalpha():
            cabinetName = "510" + self.serverName[0:3]
            
        else:
            cabinetName = "510" + self.serverName[0:2]
        for rack in racks:
            if rack["name"] == cabinetName:
                cabinetId = rack["id"]
        '''    
        return cabinetId

    def set_vlan_and_set_ips(self):
        '''This function will set the the Vlan'''
        vlan = ""
        if self.subnet.split('/')[1] == '29':
            
            vlan = "280"
            for i in range(4):
                dcim_s_r.sendRecieveDCIM("iplist.edit",{"sok": "ok", "plid": self.plid, "iptype": "public", "family": "ipv4"})
                #clicked_button=ok&domain=free.ds&family=ipv4&func=iplist.edit&ip=&iptype=public&operafake=1503243155750&plid=156&progressid=false&selected_ip_type=public&sfrom=ajax&sok=ok&zoom-ip='
                #dcim_s_r.sendRecieveDCIM("iplist",{"elid": self.plid, "sok": "ok", "elname": self.serverName})
        elif self.subnet.split('/')[1] == '30':
            vlan = "282"
        if vlan != None:
            
            dcim_s_r.sendRecieveDCIM("switch.port.edit",{"elid":  self.portId, "vlan": vlan, "sok": "ok"})
    
    def run(self):
        '''This method just runs others methods'''
        #self.add_subnet()
        
        if self.subnet == None and self.serverName == None: # we will not proceed if No useful information is entered
           
            serverTypesList=self.print_server_types()
            for server in serverTypesList:
                print("%-4s %-20s" % (server[0], server[1]))
            print("\n\n\n")
            exit()
        
        '''
        if self.serverTypeId != None:
           
            self.serverChassisTempl = self.get_server_chassis_templ(self.print_server_types(),self.serverTypeId)
        '''
        
        if self.subnet != None:
            
            self.add_subnet()
        if self.serverName != None:
            
            
            self.mac,self.ipmiIp = self.find_mac_and_ipmi_ip()
            self.switchIP,self.switchPort = self.get_the_switch_info()
            self.serverRackId = self.get_cabinet_id()
          
            self.add_server()
            self.plid = self.get_plid()
            
            self.add_ipmi()
            self.switchId,self.portId = self.add_connections()
        if self.serverName and self.subnet:
            self.set_vlan_and_set_ips()
        
        
def main():

    parser = argparse.ArgumentParser(usage="running this program without arguments will give you a list of servers types")
    parser.add_argument('-s', '--cidr',  help='Please provide a subnet in order to add this subnet into DCI manager', type=str,dest='subnet')
    parser.add_argument('-S', '--server-name', help='Please provide a server name', type=str, dest='serverName')
    parser.add_argument('-I', '--server-type-id', help='Please provide a server type id, run this script without parameters to see Ids', type=str, dest='serverTypeId')
    parser.add_argument('-H', '--hostname', help='Please provide a server hostname in order to set hostname', type=str,dest='hostname',default='free.ds')
    parser.add_argument('-U', '--ipmi-user', help='Please provide an IPMI username', type=str,dest='ipmiUser',default='root')
    parser.add_argument('-P', '--ipmi-password', help='Please provide an IPMI password', type=str,dest='ipmiPassword',default='freefromwg40')
    parser.add_argument('-v', '--vlan', help='Please provide  a Vlan ID', type=str,dest='vlan',default='998')

    args = parser.parse_args()
    #parser.print_help()
    
   
    

    addServer = AddServer(args.subnet,args.serverName,args.serverTypeId,args.hostname,args.ipmiUser,args.ipmiPassword,args.vlan)

    if vars(args).values()[0] == None and  vars(args).values()[1] == None :
        parser.print_help()
        print("\n")
        serverTypesList=addServer.print_server_types()
        for server in serverTypesList:
        
            
            print("%-4s %-20s" % (server[0], server[1]))
    
        print("\n")
  
    addServer.run()
  
if __name__ == '__main__':

    main()