import src.thread
import src.database
import ctypes
libgcc_s = ctypes.CDLL('libgcc_s.so.1')

while True:
    db = src.database.DatabaseSQL("localhost", "minecraft_scanner", "minecraft-scanner", "6G1lI5BFYVvUM3Fr4opD")
    tr = src.thread.ThreadHandler(db, progress_cache="progress")

    tr.scan_ranges(open("/root/ips.txt").readlines(), 768)
    os.remove("progress")
