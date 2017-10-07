import requests
import json

def sendRecieveDCIM(mainFunctionTosend,funcToSend):

    baseUrl = "http://68.64.160.70:1500/dcimgr?authinfo=admin:password&out=JSONdata"
   
    firstPart = {"func":  mainFunctionTosend}
    firstPart = list(firstPart.items())
    secondPart = list(funcToSend.items())
    payload  =  dict( firstPart + secondPart)
    #print payload           
    s = requests.get(baseUrl,params=payload)
    print (s.url)
    try:
        return s.json()
    except ValueError:
        return "What????"
if __name__ == "__main__":
    from pprint import pprint
    pprint(sendRecieveDCIM("rack",{}))
    #pprint(list(filter((lambda x: x if x["id"] == "9" else None),switches))[0])
    '''
    switchPort="Gi0/8"
    if switchPort[:2] == "Gi":
        switchPort = "GigabitEthernet" + switchPort[2:]
    else:
        switchPort = "FastEthernet" + switchPort[2:]
    print(switchPort)

    racks = sendRecieveDCIM("rack",{})
    for rack in racks:
        if rack["name"] == "710A4":
            print(rack["id"])
    print(list(filter((lambda x: x if x['name'] == "710A4" else None),racks))[0]['id'])
    pprint(sendRecieveDCIM("switch.port",{"elid": 48}))
    '''
    '''
    import collections
    serverList = sendRecieveDCIM("server",{})
    serverTypes = {}
    for server in serverList:
        if server['chassis_templ'] not in serverTypes.keys() and server['hostname'] == 'free.ds':
            serverTypes[server['chassis_templ']] = ["",""]
            serverTypes[server['chassis_templ']][0] = 1
            serverTypes[server['chassis_templ']][1] = server['gen_chassis_name']
        elif server['hostname'] == 'free.ds':
            serverTypes[server['chassis_templ']][0] += 1
    
    print("Server type                 Quinity    Description" )
    serverTypes = collections.OrderedDict(sorted(serverTypes.items()))
    #print(serverTypes.items())
    for serverType,server in list(serverTypes.items()):
        print("%-25s %10s %-30s" %(serverType,server[0], server[1]))
        
    ##print sendRecieveDCIM("chassistempl",{})[0]
    '''