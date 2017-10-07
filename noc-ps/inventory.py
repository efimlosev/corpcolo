#!/usr/bin/python
from json_p_n import sendRecieve as sr
placeholderGetAvaliable = [] 
#msgL = [] 
#msg2L = []
#msg3L = []

placeholderCancelandReclaim = []
def get_avaliable_servers():
    msgL = []
    
    serversModels = {}
    ServersModelsDescriptions = {}
    ''' This function returns list like this one
    ['\nName of the servers:  E3-1220v5 (Earth) Servers in the pool:    3 \nName of the servers:  E3-1240v5 (Venus) Servers in the pool:    1 \nName of the servers:  E3-1280v5 (Mercury) Servers in the pool:    1 \nName of the servers:  E5-1620 V3 Servers in the pool:    0 \nName of the servers:  E5-2603 V3 Servers in the pool:    3 \nName of the servers:  E5-2620v4 (Saturn) Servers in the pool:    1 \nName of the servers:  E5-2630L (Spring Fever) Servers in the pool:    0 \nName of the servers:  E5-2630v4 (Jupiter) Servers in the pool:    1 \nName of the servers:  E5620 Servers in the pool:    8 \nName of the servers:  L5520/L5630/E5540 Servers in the pool:    5 \nName of the servers:  L5639/X5650 (Neptune & Mars) Servers in the pool:   21 ', {1: ['L5520', 'L5630', 'E5540'], 42: ['E5-1620'], 43: ['E5-2603'], 44: ['E5-2620v4'], 51: ['E5-2630v4'], 52: ['E3-1220v5'], 53: ['E3-1240v5'], 54: ['E5-2630L'], 55: ['E3-1280v5'], 10: ['L5639', 'X5650'], 21: ['E5620']}]
    '''
    
    pools = sr("getPools")['result']['data']
    av = 'Available'
    for pool in pools:
        pool['name'] = str(pool['name'])
        if av in pool['name']:
             serversIn = numServersInthePool(pool['id'])
             msgL.append('''\nName of the servers:  %s Servers in the pool: %4d ''' % (pool['name'][10:], serversIn))
             serversModels[pool['id']] = (getModel(pool['name']))
             ServersModelsDescriptions[pool['id']] = pool['name'][10:]
    msg = ''.join(msgL)
    placeholderGetAvaliable.append(msg)
    placeholderGetAvaliable.append(serversModels)
    placeholderGetAvaliable.append(ServersModelsDescriptions)
    return  placeholderGetAvaliable
def get_server_in_reclaim_and_cancellations(servertype):
    reclaimPoolIn = sr("searchHosts",{'start': 0, 'limit': 100000, 'pool': 9})['result']['data']
    cancelPoolIn = sr("searchHosts",{'start': 0, 'limit': 100000, 'pool': 20})['result']['data']
    serverInReclaim = {}
    serverInCancel = {}
    for pId,types in servertype.iteritems():
        
         serverInReclaim[pId] = 0 
         serverInCancel[pId] = 0
         for mem in types:
           
             #reclaimPoolIn = sr("searchHosts",{'start': 0, 'limit': 100000, 'pool': 9})['result']['data']
             for reclaimM in reclaimPoolIn:
                 if mem in reclaimM['descr']:
                     serverInReclaim[pId] += 1
             for cancelM in  cancelPoolIn:
                  if mem in cancelM['descr']:
                      serverInCancel[pId] += 1
    placeholderCancelandReclaim.append(serverInReclaim)
    placeholderCancelandReclaim.append(serverInCancel)
    return placeholderCancelandReclaim

def numServersInthePool(poolid):
    ''' This functions returns number of servers with provided Id'''
    serversIn = sr("searchHosts",{'start': 0, 'limit': 100000, 'pool': poolid})['result']['total']
    return serversIn

def getModel(poolName):
    poolName = poolName[10:]
    searchList = poolName.split('/')
    lastMemberOfSL= searchList[-1].split(' ')[0]
    searchList[-1] = lastMemberOfSL
    return searchList

def getReadyToPrint():
    msg2L = []
    msg3L = []
    msgFirstPart = get_avaliable_servers()[0]
    msgFirstPart =  'Servers in Avaluable pools\n' + msgFirstPart
    reclaim = get_server_in_reclaim_and_cancellations(get_avaliable_servers()[1])[0]#return dictionary of avalible servers in reclaim pool

    for i in reclaim:
         if reclaim[i] != 0:
       #  print '''\nName of the servers:  %s Servers in the pool: %4d ''' % (get_avaliable_servers()[2][i],reclaim[i])
             msg2L.append('''\nName of the servers:  %s Servers in the pool: %4d ''' % (get_avaliable_servers()[2][i],reclaim[i]))
    msgSecondPart = ''.join(msg2L)
    
    msgSecondPart = '\nServers in Reclaim pool\n' + msgSecondPart
    cancel = get_server_in_reclaim_and_cancellations(get_avaliable_servers()[1])[1]
 
    for i in cancel:
         if cancel[i] != 0:
       #  print '''\nName of the servers:  %s Servers in the pool: %4d ''' % (get_avaliable_servers()[2][i],reclaim[i])
             msg3L.append('''\nName of the servers:  %s Servers in the pool: %4d ''' % (get_avaliable_servers()[2][i],cancel[i]))
    msgThirdPart = ''.join(msg3L)
    
    msgThirdPart = '\nServers in Cancellation pool\n' + msgThirdPart
    msg = msgFirstPart + msgSecondPart + msgThirdPart
    return msg
print getReadyToPrint()
#print get_server_in_reclaim_and_cancellations(get_avaliable_servers()[1])
#print get_avaliable_servers()[2]    
