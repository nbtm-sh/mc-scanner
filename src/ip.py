import socket, struct

class IP:
    @staticmethod
    def verify_net(net: str):
        if '/' not in net:
            return False
        
        if int(net.split('/')[1]) > 32:
            return False
        
        if len(net.split('/')[0].split('.')) != 4:
            return False;

        return True

    @staticmethod
    def generate_range(net: str):
        ##if not IP.verify_net(net):
        #    raise IP.InvalidIPException("IP address must be in xxx.xxx.xxx.xxx/yy format.")
        
        net_base = net.split('/')[0]
        mask = int(net.split('/')[1])
        mask = '1'*mask + '0'*(32-mask)
        mask = int(mask, 2)

        net_base = struct.unpack("!L", socket.inet_aton(net_base))[0]

        lower_address = net_base & mask
        upper_address = net_base | (mask ^ 4294967295)

        return_range = []

        for i in range(lower_address + 1, upper_address):
            return_range.append(socket.inet_ntoa(struct.pack('!L', i)))
        
        return return_range

    class InvalidIPException(Exception):
        pass