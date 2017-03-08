#!/bin/bash
. configure_cisco_switch.config
echo $PASSWORD
if [ "$#" -ne 4 ]
then
    echo $#
    echo "Usage $0 switch name or ip  int vlan description"
    exit
fi

  function SSH {
#Using SSH to  configure cisco's port
sshpass -p $PASSWORD ssh -l $LOGIN -oKexAlgorithms=+diffie-hellman-group1-sha1  $HOST << EOF
 conf t
 int $INT
 sw acc vl $VL
 desc $DESC
no  sh
 exit 
 exit
 wr
 exit 
EOF
}

 function TELNET {
#Using SSH to  configure cisco's port
echo "$LOGIN
$PASSWORD
conf t
 int $INT
 sw acc vl $VL
 desc $DESC
no  sh
 exit 
 exit
 wr
 exit 
 " | nc $HOST 23
}
nc -z -w2 $HOST 22
if [ $? -eq 0 ]
  then
  echo 'ssh works'
  SSH 
  else
  echo 'ssh does not work'
  TELNET
fi


