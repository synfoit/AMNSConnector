import os
from threading import Thread

import snap7
from snap7.exceptions import Snap7Exception
from snap7.util import *
from snap7.types import *


class PLC_DB_Connection(Thread):


    def ReadMemory(self,plc, DB_NUMBER, START_ADDRESS, SIZE, datatype):
        # define read memory function
        result = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
        if datatype == S7WLBit:
            return get_bool(result, 0, 1)
        elif datatype == S7WLByte or datatype == S7WLWord:
            return get_int(result, 0)
        elif datatype == S7WLReal:
            return get_real(result, 0)
        elif datatype == S7WLDWord:
            return get_dword(result, 0)
        elif datatype == S7WLInt:
            return get_int(result, 0)
        else:
            return None

    def ReadData(self):
        IP = '172.16.162.12'  # IP plc
        RACK = 0  # RACK PLC
        SLOT = 3  # SLOT PLC
        slabNumner='amns'
        try:
            plc = snap7.client.Client()  # call snap7 client function
            plc.connect(IP, RACK, SLOT)  # connect to plc

            state = plc.get_cpu_state()  # read plc state run/stop/error
            print("plcstatus",state)
            caster_length = 0
            slab_no = 0
            caster_speed = 0
            slab_length = 0
            caster_width = 0
            caster_thikness = 0
            castermode = 0

            while True:
                now = datetime.now()
                if state != 'S7CpuStatusRun':
                    try:
                        plc = snap7.client.Client()  # call snap7 client function
                        plc.connect(IP, RACK, SLOT) # ('IP-address', rack, slot)
                        print('not connected')
                        time.sleep(0.2)
                    except Snap7Exception as e:
                        self.ReadData()
                else:
                    print('connected')

                caster_length = self.ReadMemory(plc, 880, 320, 4, S7WLReal)
                slab_no = self.ReadMemory(plc, 880, 220, 4, S7WLReal)
                caster_speed = self.ReadMemory(plc, 880, 4, 4, S7WLReal)
                slab_length = self.ReadMemory(plc, 880, 8, 4, S7WLReal)
                caster_width = self.ReadMemory(plc, 880, 346, 4, S7WLReal)
                caster_thikness = self.ReadMemory(plc, 110, 0, 4, S7WLReal)
                casterwidth = self.ReadMemory(plc, 110, 4, 4, S7WLReal)
                castermode = self.ReadMemory(plc, 110, 8, 4, S7WLReal)

                # Data to be written
                dictionary = [
                    caster_length,
                    slab_no,
                    caster_speed,
                    slab_length,
                    caster_width,
                    caster_thikness,
                    casterwidth,
                    castermode

                ]

                # Serializing json
                data = str(dictionary).replace('[', '').replace(']', '').replace(',', ' ').replace(',', ' ')

                # Writing to sample.json
                if os.path.exists('C:/.amns/LiveData/plc_data.txt'):
                    fileSize = os.path.getsize('C:/.amns/LiveData/plc_data.txt')
                    if fileSize > 50000000:
                        os.remove('C:/.amns/LiveData/plc_data.txt')
                    else:
                        with open('C:/.amns/LiveData/plc_data.txt', 'a') as f:
                            f.write(data + '\n')
                else:
                    with open('C:/.amns/LiveData/plc_data.txt', 'a') as f:
                        f.write(data + '\n')

                if(slabNumner!=slab_no):
                    newfileName = now.strftime("_%d_%m_%Y_%H_%M")
                    dictionarysave = [
                        caster_length,
                        slab_no,
                        caster_speed,
                        slab_length,
                        caster_width,
                        caster_thikness,
                        casterwidth,
                        castermode,
                        'Slab_'+str(slab_no).replace(".0", '')+newfileName

                    ]

                    # Serializing json
                    data = str(dictionarysave).replace('[', '').replace(']', '').replace(',', ' ').replace(',', ' ')
                    with open('C:/Users/Admin/Documents/data/plc_data.txt', 'a') as f:
                        f.write(data + '\n')
                slabNumner=slab_no
                time.sleep(1)
        except:
            self.ReadData()

    def run(self) -> None:
        plcdb = PLC_DB_Connection()
        plcdb.ReadData()
        time.sleep(1)


