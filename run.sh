#!/bin/bash

echo "Slave 1.........Starting"
python Berkeley.py -s ip=127.0.0.1 port=7000 time=2:20:15 logfile=clock.log &

#echo "Slave 2.........Starting"
#python Berkeley.py -s ip=127.0.0.1 port=7002 time=2:35:01 logfile=clock.log &

#echo "Slave 3.........Starting"
#python Berkeley.py -s ip=127.0.0.1 port=7003 time=2:23:19 logfile=clock.log &

#delta is seconds (d)
echo "Master..........Starting"
python Berkeley.py -m ip=127.0.0.1 port=6999 time=2:26:55 logfile=clock.log d=1200

 

