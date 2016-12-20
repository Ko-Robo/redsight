# RASPI
## abstract
 raspberry pi(raspi) is a main intellect of this system, which processes image-processing, neural-net, communicating other hardware modules and so on.
 because of  its high level enviroment,  we think that using raspi make it easy  to programm it  than OS-less environment.
 
## equipments 
- rapsberry pi 3b
- sd-card (more than 16GB)


require to setupping
- monitor
- (mouse)
- keyboard

## setup 
#### OS install
this time, we used NOOBOS Raspbian
#### network config
[ref] [Automatically connect a Raspberry Pi to a Wifi network](http://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/)
after "Configuring WiFi connection" of above link, make ssh enable in raspi-config ```$ sudo raspi-config # advantaged option -> ssh -> enable```

next, check if we can connect raspi using ssh
```
# in raspi
$ ifconfig # or /sbin/ifconfig
.....
wlanX     ..... 
          inet addr:X.X.X.X  Bcast:X.X.X.X  Mask:X.X.X.X
```
the "inet" of the source means ipv4 (local)address of raspberry pi. memo inet, type ssh command.
```
# in client
$ ssh pi@addr # addr (X.X.X.X)
```

#### user config
[ref] [How to create a new user on Raspberry Pi](http://raspi.tv/2012/how-to-create-a-new-user-on-raspberry-pi)
1. adduser. 
```
$ sudo adduser <new-user>
```
2. authorize-config. make new-user to forgive to become root
```
$sudo visudo
pi ALL=(ALL) ALL
<new-user> ALL=(ALL) ALL     # change line of new-user
```
3. test if it is able for new user to become root
```
$ login <new-user>
$ sudo
```
4. delet user "pi"
```
$ sudo deluser -remove-home pi
```

#### Installing this system
please read INSTALL.md

#### test