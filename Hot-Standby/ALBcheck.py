#!/bin/bash
linecount=0
while true; do
	echo " " > output.txt
       	ping -c2 192.168.5.1 >> output.txt
	linecount=$(sed -n '/100% packet loss/p ' output.txt | wc -l)
	echo $linecount
	if [ $linecount -eq 1 ]
	then
		
       		ip link set dev eth21 up	
		ip link set dev eth11 up
		python anycastloadbalancer.py -f1 5 -f2 60 -t 1
	fi
	sleep 5;
done
