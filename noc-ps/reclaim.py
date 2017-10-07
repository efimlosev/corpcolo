#!/usr/bin/python

import subprocess
import re
pattern_7th_floor = '^(710[AB])[0-9]{1,2}R[0-9]{1,2}.' 
from json_p_n import sendRecieve as sr
def Main():
    p_it =  print_subnet(args.subnet)
    print "%s %s %s \"%s\"" % (p_it[0],p_it[1],p_it[2],p_it[3])

    subprocess.check_call(['/home/efim/Dropbox/sshs_rem.sh', p_it[0], p_it[1], str(p_it[2]), p_it[3]])

def getSubnets():
    just_networks = []
    dict_subnets = sr("getSubnets", 0 ,9999)['result']#TEMP
    total_subnets =  dict_subnets['total']
    print total_subnets
    for i in range(total_subnets):
        just_networks.append(dict_subnets['data'][i]['subnet'])
    return just_networks

def getFirstHostfromEachNetwork():
    subnets_we_need_only = {}
    subnets = getSubnets()
    for subnet in subnets:
        
        try:
            tmp = sr("getHosts",subnet,1,1)['result']['data'][0]
            if tmp['pool'] == 9:    
#                print "%s %s" %  (tmp['descr'],tmp['pool'])
                if re.match(pattern_7th_floor,tmp['descr']):
                   print "7th"
                else:
                   print "5th" 

        except:
            pass
          
        
          
        #if sr("getHosts",subnet,1,1)['result']['data'][0]['pool]' == 9: #reclaim pool
         #    subnets_we_need_only.append(subnet)
            

#    print subnets_we_need_only[subnet] 


getFirstHostfromEachNetwork()
