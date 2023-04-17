import src.server
from time import strftime, localtime
import mysql.connector

class Database:
    def __init__(self, **kwargs):
        pass

    def write_row(self, row_object : src.server.ServerObject):
        pass

class DatabaseSQL(Database):
    def __init__(self, database_ip, database_name, database_user, database_password):
        self.database_connection = mysql.connector.connect(
                host=database_ip,
                user=database_user,
                passwd=database_password,
                database=database_name
                )

    def write_row(self, row_object : src.server.ServerObject):
            scan_time = strftime('%Y-%m-%d %H:%M:%S', localtime(row_object.scan_time))
            row_object.country = str(row_object.country)[0:2]
            row_object.latency = str(row_object.latency)[0:3]
            row_object.description = row_object.description.replace("'", "")
            row = row_object
            db_query = f"INSERT INTO `scan_results` (`fingerprint`, `ipAddress`, `port`, `motd`, `country`, `reg`, `city`, `isp`, `latency`, `onlinePlayers`, `favicon`, `scanTime`) VALUES ('{row_object.get_fingerprint()}', '{row_object.ip_address}', {row_object.port}, '{row.description}', '{row.country}', '{row.region}', '{row.city}', '{row.isp}', '{row.latency}', '{row.online_players}', '{row.favicon}', '{scan_time}');"

            cur = self.database_connection.cursor()
            cur.execute(db_query);
            self.database_connection.commit()
            cur.close()


class DatabaseCSV(Database):
    def __init__(self, file_name):
        self.f = open(file_name, "w")
        """self.description = description
        self.favicon = favicon
        self.latency = latency
        self.max_players = max_players
        self.online_players = online_players
        self.sample_players = sample_players
        self.hostname = None
        self.city = None
        self.region = None
        self.country = None
        self.isp = None"""
    
    def write_row(self, row_object):
        write_data = f"{row_object.get_fingerprint()},{row_object.scan_time},{row_object.ip_address},{row_object.port},{row_object.version},{row_object.country},{row_object.city},{row_object.region}\n"
        self.f.write(write_data)
        self.f.flush()
