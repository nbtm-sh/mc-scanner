from mcstatus import JavaServer
import hashlib, requests, json, time, socket

class Server:
    @staticmethod
    def is_server(ip_address: str, port: int):
        if Server.port_open(ip_address, port):
            test_server = JavaServer.lookup(f"{ip_address}:{str(port)}")
            try:
                test_server.status()
                return True
            except:
                return False
        else:
            return False

    @staticmethod
    def get_server(ip_address: str, port = 25565):
        test_server = JavaServer.lookup(f"{ip_address}:{str(port)}")
        status = test_server.status()

        return ServerObject(
            ip_address,
            port,
            status.description,
            status.favicon,
            status.latency,
            status.players.max,
            status.players.online,
            str([]),
            status.version.name
        )

    @staticmethod
    def port_open(ip_address: str, port = 25565):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip_address, port))
            sock.close()
            return True
        except:
            return False 

class ServerObject:
    def __init__(self, ip_address, port, description, favicon, latency, max_players, online_players, sample_players, version, scan_time = None):
        self.description = description
        self.favicon = favicon
        self.latency = latency
        self.max_players = max_players
        self.online_players = online_players
        self.sample_players = sample_players
        self.version = version
        self.ip_address = ip_address
        self.port = port
        self.hostname = None
        self.city = None
        self.region = None
        self.country = None
        self.isp = None
        self.scan_time = scan_time if scan_time is not None else int(time.time())

        # Get IP info
        try:
            j_data = requests.get(f"https://ipinfo.io/{ip_address}/json").json()

            self.hostname = j_data["hostname"]
            self.city = j_data["city"]
            self.region = j_data["region"]
            self.country = j_data["country"]
            self.isp = ' '.join(j_data["org"].split(' ')[1:])
        except:
            pass
        
    def get_fingerprint(self):
        try:
            return hashlib.md5(bytes(str(self.version) + str(self.favicon) + str(self.max_players) + str(self.country) + str(self.region) + str (self.city) + ip_address, "UTF-8")).hexdigest()
        except:
            return ""
