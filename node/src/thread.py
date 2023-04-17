import threading
import src.database
import src.util, src.ip, src.server
import time
import os
import json

class ThreadHandler:
    def __init__(self, database : src.database.Database, progress_cache : str, clear_progress=False):
        self.database = database

        if clear_progress:
            f = open(progress_cache, "w")
            f.write("")
            f.close()

        self.progress_cache_name = progress_cache

        self.total_ips = 0
        self.scanned_ips = 0
        self.error_ips = 0
        self.current_ip = ""
        self.found_servers = 0

        self.json_progress = {}
    
    def scan_ranges(self, ip_range: list, threads_count):
        ranges_list = []
        x = 0
        y = len(ip_range)
        z = str(int(((x / y) * 100)))
        for i in ip_range:
            x += 1
            z = str(int(((x / y) * 100)))

            print(f"\rProcessing IP List: {z}%", end="") 
            ranges_list.extend(src.ip.IP.generate_range(i))
        
        # Remove IPs that have already been scanned
        x = 0
        y = threads_count 
        z = str(int((x / y) * 100))
        if os.path.isfile(self.progress_cache_name):
            print(f"\rProcessing progress list {z}%", end="")
            with open(self.progress_cache_name, "r") as f:
                self.json_progress = json.load(f)
            x = threads_count
            z = str(int((x / y) * 100))
            print(f"\rProcessing progress list: {z}%", end="")

        else:
            # Create the file
            for i in range(threads_count):
                print(f"\rProcessing progress list: {z}%", end="")
                x += 1
                self.json_progress[str(i)] = 0
                
        self.total_ips = len(ranges_list)
        self.scanned_ips = sum(self.json_progress.values())
        
        ranges_list = src.util.split_array(ranges_list, threads_count)
        threads = []

        thread_i = 0

        for t in range(threads_count):
            x = threading.Thread(target=ThreadHandler.scanner, args=(thread_i, ranges_list[t],self.database,self,self.json_progress[str(thread_i)],))
            x.start()
            threads.append(x)

            thread_i += 1
        
        # Wait for all threads to finish
        prev_count = 0
        avg = [0 for i in range(500)]
        while True:
            time.sleep(0.05)
            scanned_percent = self.scanned_ips
            scanned_percent /= self.total_ips
            scanned_percent *= 100
            scanned_percent = str(int(scanned_percent)) + "%"

            diff = self.scanned_ips - prev_count
            diff *= 20
            avg.pop(0)
            avg.append(diff)

            scan_average = int(sum(avg) / len(avg))

            prev_count = self.scanned_ips
            
            print(f"\rScanning: {scanned_percent} ({self.scanned_ips} / {self.total_ips}), Found: {self.found_servers}, Error(s): {self.error_ips}, P/S: {str(scan_average)} Current IP: {self.current_ip}               ", end="")
        
        return
    
    def mark_scanned(self, ip_address):
        self.scanned_ips += 1
    
    def mark_error(self, ip_address):
        self.error_ips += 1
        self.scanned_ips += 1

    def report_progress(self, thread_id, index):
        self.json_progress[thread_id] = index
        if (self.scanned_ips % 500 == 0):
            self.write_progress()

    def write_progress(self):
        if not os.path.isfile(self.progress_cache_name):
            f = open(self.progress_cache_name, "x")
            f.close()

        json_string = json.dumps(self.json_progress)
        with open(self.progress_cache_name, "w") as f:
            f.write(json_string)
            f.flush
            f.close()
        return True
    
    @staticmethod
    def scanner(thread_id, ip_range, database : src.database.Database, th, start_index):
        index = start_index
        while True:
            try:
                while index < len(ip_range):
                    th.current_ip = ip_range[index]
                    if src.server.Server.is_server(ip_range[index], 25565):
                        database.write_row(src.server.Server.get_server(ip_range[index]))
                        th.found_servers += 1
                    th.mark_scanned(ip_range[index])
                    th.report_progress(thread_id, index)
                    index += 1
                break
            except Exception as e:
                th.mark_error(ip_range[index])
                print(e)
                index += 1
