

from Laser_Connection import LaserMainCode
from LineScanner_Connection import LineScanner
from PLC_DB_Connection import PLC_DB_Connection


plc = PLC_DB_Connection()
plc.start()
ls = LineScanner()
ls.start()
lc=LaserMainCode()
lc.start()

