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
        hosts = hosts.split('\n')
        for host in hosts:
            self.add_host(host)


    def get_hosts(self):
        return self.__hosts


    def add_host(self, host):
        self.__hosts.append(host)


    def remove_host(self, host):
        self.__hosts.remove(host)


def master():
    pass


def slave():
    pass


def main(argv):
    conf = Configuration()

    # create logging
    logger = logging.getLogger('clock')
    logger.setLevel(logging.DEBUG)

    # create file
    fh = logging.FileHandler('clock.log')
    fh.setLevel(logging.DEBUG)

    # create on screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # create handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(conf.get_ip() + ':' + conf.get_port() + ' STARTING')

    if (conf.get_mode() in '-m'):
        logger.info(conf.get_ip() + ':' + conf.get_port() + ' MODE: Master')
        master()
        conf.read_hosts('clients.txt')
        hosts = conf.get_hosts()
        for host in hosts:
            host = host.split(':')
            try:
                ip   = host[0]
                port = host[1]
            except IndexError as ex:
                pass
    if (conf.get_mode() in '-s'):
        logger.info(conf.get_ip() + ':' + conf.get_port() + ' MODE: Slave')
        slave()


if __name__ == '__main__':

    sys.argv.append('-m')
    sys.argv.append('port=6999')
    sys.argv.append('ip=127.0.0.1')
    main(sys.argv)

