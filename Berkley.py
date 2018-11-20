'''
@author: Allan Gustavo Fernandes - 31568211
@author: Fabio Shimada Pinto     - 31160344
'''

import sys
import socket
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

def client(self, msg, ip, port):
    print "UDP target IP:", ip
    print "UDP target port:", port()
    print "message:", msg

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (ip, port))


def main(argv):
    conf = Configuration()
    time = time.strftime('%X %x')
    #server("test", conf.get_ip(), conf.get_port())


if __name__ == "__main__":
    '''
        Reconhecer entrada, -m master, -s slave
    '''
    sys.argv.append('-m')
    sys.argv.append('port=7000')
    sys.argv.append('ip=10.0.0.1')
    main(sys.argv)