'''
@author: Allan Gustavo Fernandes - 31568211
@author: Fabio Shimada Pinto     - 31160344
'''

import sys
import socket
import logging
import time

class Configuration:

    def __init__(self):
        conf = {}
        for arg in sys.argv:
            if arg in ["-m", "-s"]:
                self.__mode = arg
            arg = arg.split("=")
            try:
                conf[arg[0]] = arg[1]
            except IndexError:
                pass
        self.__ip      = conf.get("ip")
        self.__port    = conf.get("port")
        self.__time    = conf.get("time")
        self.__delta   = conf.get("d")
        self.__logfile = conf.get("logfile")
        self.__hosts   = []


    def get_mode(self):
        return self.__mode


    def get_ip(self):
        return self.__ip


    def get_port(self):
        return self.__port


    def get_time(self):
        return self.__time


    def set_time(self, time):
        self.__time = time


    def get_delta(self):
        return self.__delta


    def get_logfile(self):
        return self.__logfile


    def read_hosts(self, file):
        hosts = open(file).read()
        hosts = hosts.split('\n')
        for host in hosts:
            self.add_host(host)


    def get_hosts(self):
        return self.__hosts


    def add_host(self, host):
        self.__hosts.append(host)


    def remove_host(self, host):
        self.__hosts.remove(host)


def main(argv):
    conf = Configuration()

    # create logging
    logger = logging.getLogger('clock')
    logger.setLevel(logging.DEBUG)

    # create file
    fh = logging.FileHandler(conf.get_logfile())
    fh.setLevel(logging.DEBUG)

    # create on screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s | %(name)s - %(levelname)s - Berkeley: ' + conf.get_time() + ' - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # create handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(conf.get_ip() + ':' + conf.get_port() + ' STARTING')

    if (conf.get_mode() in '-m'):
        logger.info(conf.get_ip() + ':' + conf.get_port() + ' MODE: Master')
        # starting master
        conf.read_hosts('clients.txt')
        hosts = conf.get_hosts()
        while True:
            # wait end show logs
            time.sleep(1)
            msg = raw_input("command_: ")
            for host in hosts:
                host = host.split(':')
                masterSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    ip   = host[0]
                    port = host[1]
                except IndexError:
                    pass
                #REMOVER
                print port
                masterSock.sendto(str(msg), (ip, int(port)))
                data, addr = masterSock.recvfrom(1024)
                # REMOVER DO CODIGO
                print 'answer:'
                print data
                masterSock.close()
                if 'quit' in msg:
                    sys.exit(0)

    if (conf.get_mode() in '-s'):
        logger.info(conf.get_ip() + ':' + conf.get_port() + ' MODE: Slave')
        # starting slave
        slaveSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        slaveSock.bind(('0.0.0.0', int(conf.get_port())))
        while True:
            data, addr = slaveSock.recvfrom(1024)
            if 'quit' in data:
                slaveSock.close()
                sys.exit(0)
            if 'get_time' in data:
                slaveSock.sendto(conf.get_time(), addr)

if __name__ == '__main__':

    '''
    REMOVE BEFORE FLY
    
    '''
    #sys.argv.append('-m')
    #sys.argv.append('port=6999')
    #sys.argv.append('ip=127.0.0.1')
    #sys.argv.append('time=2:20:15')
    #sys.argv.append('d=5')
    #sys.argv.append('logfile=clock.log')

    main(sys.argv)
