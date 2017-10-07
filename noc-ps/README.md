# This file will describe my script in this folder

1. json_p_n.py - a simple library which helps to send requests to your  NOC -PS provistion system.
2. password.py - we need this file to make our main library work. 
3. inventory.ry My bosses wanted me to know how many servers are available.  it is ugly,  those days I didn't have enough experience.
4. reclaim.py - This script helps reclaim unused server. It [requires](https://github.com/efimlosev/corpcolo/tree/master/cabinetswitches) it does:
  * Clears  server  customers' information.
  * Deletes Used  Servers' IP.
  * Delete  Subnets which are not in use anymore.
  * Set Swiches' VLAN as it was before customers

 
