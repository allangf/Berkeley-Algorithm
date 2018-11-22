import socket
fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
udp_ip = '127.0.0.1'
udp_port = 8014
while(True):
    message = input("Client :")
    fd.sendto(message, (udp_ip, udp_port))
    reply = fd.recvfrom(1000)
    print("Server:%s"%(reply))
