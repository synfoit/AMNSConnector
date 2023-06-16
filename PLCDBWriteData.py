
import snap7
from snap7.util import *
from snap7.types import *

from loggerFile import LoggerData


class PLCDBWriteData:
    def WriteMemory(self, plc, DB_NUMBER, START_ADDRESS, SIZE,datatype,value):
        # define read memory function
        result = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
        if datatype == S7WLBit:
            set_bool(result, 0, 1,value)
            plc.db_write(DB_NUMBER,START_ADDRESS,result)
        elif datatype == S7WLByte or datatype == S7WLWord:
             set_int(result, 0,value)
             plc.db_write(DB_NUMBER, START_ADDRESS, result)
        elif datatype == S7WLReal:
             set_real(result, 0,value)
             plc.db_write(DB_NUMBER, START_ADDRESS, result)
        elif datatype == S7WLDWord:
             set_dword(result, 0,value)
             plc.db_write(DB_NUMBER, START_ADDRESS, result)
        elif datatype == S7WLInt:
             set_int(result, 0,value)
             plc.db_write(DB_NUMBER, START_ADDRESS, result)


    def WriteData(self,thinkness1avg,thinkness2avg,slab1avg,slab2avg,p1,p2,p3,p4,p5,t1,t2):

        try:
            IP = '172.16.162.12'  # IP plc
            RACK = 0  # RACK PLC
            SLOT = 3  # SLOT PLC
            PORT=810

            plc = snap7.client.Client()  # call snap7 client function
            plc.connect(IP, RACK, SLOT)  # connect to plc

            state = plc.get_cpu_state()  # read plc state run/stop/error

            self.WriteMemory(plc, 111, 0, 4, S7WLReal, thinkness1avg)
            self.WriteMemory(plc, 111, 4, 4, S7WLReal, thinkness2avg)
            self.WriteMemory(plc, 111, 8, 4, S7WLReal, slab1avg)
            self.WriteMemory(plc, 111, 12, 4, S7WLReal, slab2avg)
            self.WriteMemory(plc, 111, 16, 4, S7WLReal, p1)
            self.WriteMemory(plc, 111, 20, 4, S7WLReal, p2)
            self.WriteMemory(plc, 111, 24, 4, S7WLReal, p3)
            self.WriteMemory(plc, 111, 28, 4, S7WLReal, p4)
            self.WriteMemory(plc, 111, 32, 4, S7WLReal, p5)
            self.WriteMemory(plc, 111, 36, 4, S7WLReal, t1)
            self.WriteMemory(plc, 111, 40, 4, S7WLReal, t2)
        except:
            LoggerData().logger.error("PLC write loss connection")
            self.WriteData(thinkness1avg,thinkness2avg,slab1avg,slab2avg,p1,p2,p3,p4,p5,t1,t2)

