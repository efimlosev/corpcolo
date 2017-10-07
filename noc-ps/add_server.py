from json_p_n import sendRecieve

import pexpect,argparse
from sys import path
import subprocess

path.append('/home/efim/Dropbox')
from  ipcalc_flask import calculateSubnet as calc
def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('subnet', help='Give me a subnet', type=str) #optinal argument
    parser.add_argument('vlan', help='We need a vlan here', type=str) #the same

    parser.add_argument('desc', help='We need a description here', type=str) #the same
    
    parser.add_argument('hostname', nargs='?', help='We need a hostname here', type=str) #the same
    parser.add_argument('-i', help='We need an Ip here', type=str) #the same


    args = parser.parse_args()
    temp = addUrl(args.subnet,args.vlan,args.desc)
    temp1 = getAllinformationWeWantiToUpdate(temp,{'hostname': args.hostname},args.i)
    updateHost(temp1,args.vlan,args.desc)
def addUrl(subnet,vlan,desc):
    tmp = calc(subnet)
    sub = str(tmp[0])
    gw = str(tmp[1])
    ip = str(tmp[2]).split(' - ')[0]
    nm = str(tmp[3])
    servername, descrend = desc.split(' ')
    tmp = None
    tmp = sendRecieve('addSubnet',{'subnet': sub, 'gateway': gw, 'netmask': nm, 'vlan' : vlan, 'description': desc})
    print tmp['result']['success']
    ipSub = { 'ip':ip, 'subnet': sub, 'descrend' : descrend, 'servername' : servername }
    return ipSub
def getAllinformationWeWantiToUpdate(ipsub,hostname,ip=None):
    ipsub.update(hostname)
    if ip != None:
        ipsub['ip'] = ip
   # print ipsub
    return ipsub
def updateHost(whatWeWantToUpdate,vlan,desc ):
   hosts = sendRecieve("searchHosts", {'start': 0, 'limit': 100, 'query': whatWeWantToUpdate['servername'] })['result']['data']
      
   exactHost = [ host for host  in hosts if host['descr'].split('(')[0] == whatWeWantToUpdate['servername']] 
   #print exactHost[0]['descr']
   for k,v in exactHost[0].iteritems():
       if  k  in whatWeWantToUpdate:
           exactHost[0][k] = whatWeWantToUpdate[k]
   
   exactHost[0]['descr'] = str(exactHost[0]['descr'].split(')')[0] + ')' + whatWeWantToUpdate['descrend'])
   print  exactHost[0]['pool']
   connection = sendRecieve("getConnectionsByHost", exactHost[0]['mac'])['result']['data']
   switchName = connection[0]['devname']
   switchPort = connection[0]['portdescr'].split(' ')[1].split('[')[1].split(']')[0]
   devices = sendRecieve("getDevices", 0, 1000)['result']['data']
   switchIp = [device['ip'] for device in devices  if device['name'] == switchName ][0] 

   if exactHost[0]['pool'] != 16:
       print 'Something went wrong, exitting!'
       exit()
   print sendRecieve("getConnectionsByHost", exactHost[0]['mac'])
   print  exactHost[0]['ip']
   print  sendRecieve("updateHost",  exactHost[0])
   subprocess.check_call(['/home/efim/Dropbox/sshs_rem.sh',  switchIp,  switchPort,  vlan, desc])
if __name__ == '__main__':
   Main()
   #updateHost('710A6R22', {'descr': 'test'})  

 
