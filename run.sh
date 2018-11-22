#!/bin/bash

echo "Slave 1.........Starting"
python Berkeley.py -s ip=127.0.0.1 port=7000 time=2:20:15

echo "Slave 2.........Starting"
python Berkeley.py -s ip=127.0.0.1 port=7002 time=2:35:01

echo "Slave 3.........Starting"
python Berkeley.py -s ip=127.0.0.1 port=7003 time=2:23:19

echo "Master..........Starting"
python Berkeley.py -m ip=127.0.0.1 port=6999 time=2:26:55 logfile=clock.log d=5

 

