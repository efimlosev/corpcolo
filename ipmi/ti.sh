IP=$1;
NAME=$2;
PASS=$3;
RP="Put a root password here"
if
[ "$#" -ne 3 ]
then
echo "Usage $0 IP NAME PASSWORD"
exit
fi
ipmitool -Ilanplus -Uroot -P$RP -H$IP user set name 3 $NAME
ipmitool -Ilanplus -Uroot -P$RP -H$IP user set password 3 $PASS
ipmitool -Ilanplus -Uroot -P$RP -H$IP user enable 3
