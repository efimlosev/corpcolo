# This Script should help you to configure cisco switches.

It was tested on cisco 2960series.

You have to install two  additional program:

- netcat
- sshpass

you  have to pass paranmeters to the script in order to make it work. Please  see an example below:

``` bash
./configure_cisco_switch.sh 123.123.123.123 Gi0/24 66 "Some description"
```


Please  do not forget to set your switch login and password in "configure_cisco_switch.config"
