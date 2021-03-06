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

def tostamp(time):
    time = time.split(':')
    try:
        hour = int(time[2]) * 3600
        min = int(time[1]) * 60
        sec = int(time[0])
        return (int(hour) + int(min) + int(sec))
    except Exception:
        pass


def totime(stamp):
    hour = int((stamp % 3600) % 60)
    min = int(stamp % 3600) / 60
    sec = int(stamp / 3600)
    return str(hour) + ':' + str(min) + ':' + str(sec)


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
        count = 0
        dsum  = 0
        while True:
            avg = 0
            # wait end show logs
            time.sleep(1)
            msg = raw_input("command_: ")
            for host in hosts:
                host = host.split(':')
                master_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    ip   = host[0]
                    port = host[1]
                except IndexError:
                    pass
                master_sock.sendto(str(msg), (ip, int(port)))
                data, addr = master_sock.recvfrom(1024)
                logger.info(data)
                master_time  = conf.get_time()
                slave_time   = data
                master_stamp = tostamp(master_time)
                slave_stamp  = tostamp(slave_time)
                delta = 0
                try:
                    delta = master_stamp - slave_stamp
                except TypeError:
                    pass

                if delta < conf.get_delta():
                    count += 1
                    dsum += delta
                master_sock.close()
                if 'quit' in msg:
                    sys.exit(0)
            avg = dsum / count
            for host in hosts:
                host = host.split(':')
                master_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    ip = host[0]
                    port = host[1]
                except IndexError:
                    pass
                master_sock.sendto(str('set_time ' + avg), (ip, int(port)))
                data, addr = master_sock.recvfrom(1024)
                logger.info(data)

    if (conf.get_mode() in '-s'):
        logger.info(conf.get_ip() + ':' + conf.get_port() + ' MODE: Slave')
        # starting slave
        while True:
            slave_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            slave_sock.bind(('0.0.0.0', int(conf.get_port())))
            data, addr = slave_sock.recvfrom(1024)
            if 'quit' in data:
                slave_sock.sendto('quiting', addr)
                slave_sock.close()
                sys.exit(0)
            if 'get_time' in data:
                slave_sock.sendto(conf.get_time(), addr)
                slave_sock.close()
            if 'set_time' in data:
                data = data.split(' ')
                slave_stamp = tostamp(conf.get_time()) + data[1]
                slave_time = totime(slave_stamp)
                conf.set_time(slave_time)
                slave_sock.close()

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
