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
        self.__ip   = conf.get("ip")
        self.__port = conf.get("port")
        self.__hosts = []


    def get_mode(self):
        return self.__mode


    def get_ip(self):
        return self.__ip


    def get_port(self):
        return self.__port


    def read_hosts(self, file):
        hosts = open(file).read()
        for host in hosts:
            self.__hosts.append(host)


    def get_hosts(self):
        return  self.__hosts


    def add_host(self, host):
        self.__hosts.append(host)


    def remove_host(self, host):
        self.__hosts.remove(host)


def master(self):
    pass


def slave(self):
    pass


def main(argv):
    conf = Configuration()

    # create logger
    logger = logging.getLogger('clock-log')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info('Starting' + conf.get_ip() + ':' + conf.get_port())

    if (conf.get_mode() in '-m'):
        logger.info( conf.get_ip() + ' MODE: Master')
        master()
        conf.read_hosts('clients.txt')
    if (conf.get_mode() in '-s'):
        logger.info(conf.get_ip() + ' MODE: Slave')
        slave()


if __name__
    "__main__":

    sys.argv.append('-m')
    sys.argv.append('port=7000')
    sys.argv.append('ip=10.0.0.1')
    main(sys.argv)