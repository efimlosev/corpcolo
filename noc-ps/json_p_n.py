import requests
import json
from passwords import PassPm 
#Send Data to server
def sendRecieve(method,*params):
    url = PassPm().url
    headers = PassPm().headers 
    auth = PassPm().auth
    # Example echo method
    payload = {
        #"method": "getHosts",
        "method": method,
        #"params": ["68.64.172.232", 0, 9999],
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers, auth=auth, verify=False).json() #Load data

    
    return  response

if __name__ == "__main__":
#    from ipcalc_flask import calculateSubnet as calc
#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('subnet', help='Give me a subnet', type=str)
#    args = parser.parse_args()
#    pools  = sendRecieve("getPools")
#    for i in range (len(pools['result']['data'])):
#        print "id:  %s name: %s" %  (pools['result']['data'][i]['id'], pools['result']['data'][i]['name'])
#--------------------------------------------------------------
    reclaimL = []
    sub = []
    reclaim  = sendRecieve("searchHosts", {'start': 0, 'limit': 100000, 'pool': 9})
    subnets  = sendRecieve("getSubnets", 0, 10000)['result']['data']
    #print subnets
    for r in reclaim['result']['data']:
         reclaimL.append(r['subnet'])

    for net in subnets:
#        print net['subnet']
        if net['subnet'] in reclaimL:
            print "int vlan %s" % (net['vlan'])
            print "no ip add %s  %s sec" % (net['gw'],net['netmask'])
            print "exit" 
            sub.append(net['subnet'])
#    print sub            
#-------------------------------------------------------------



