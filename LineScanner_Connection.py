
from threading import Thread
from opcua import Client
from opcua.ua import VariantType
import json
import numpy as np
import os
import time
from datetime import datetime
from PLCDBWriteData import PLCDBWriteData
from loggerFile import LoggerData


class LineScanner(Thread):

    def __init__(self):
        super().__init__()

    def Convert(self, removeUnwantedContentS1S2):
        li = list(removeUnwantedContentS1S2.split(" "))
        return li

    def getDataFromScanner(self):
        try:
            userPath = 'C:'
            np.set_printoptions(linewidth=np.inf)
            configFilePath = 'C:\.amns\AMNSConfigFiles\ConfigFiles\Config.json'
            f = open(configFilePath)
            data = json.load(f)
            url = data['opcua']
            # print("url",url)  # opc.tcp://192.168.42.100:4840/
            client = Client(url)
            client.connect()
            # print("clent",client.connect())
            emissivity = data['emissivity']
            # Reading Config data from Config File -- Starting

            slabGlobal = "amns"
            fileToSave = "slab"
            while True:
                now = datetime.now()
                # today = date.today()
                oneDateFile = now.strftime("%d_%m_%Y")
                # print("OCP-UA Connected")
                # print(            "[WARNING] Please, do not close this Command Prompt Window, Data fetching is in process from Line Scanner !!")


                InternalTemperaturescanner1 = client.get_node("ns=1;s=InternalTemperature")
                InternalTemperaturescanner1 = InternalTemperaturescanner1.get_value()

                InternalTemperaturescanner2 = client.get_node("ns=2;s=InternalTemperature")
                InternalTemperaturescanner2 = InternalTemperaturescanner2.get_value()

                # Avg Max Value -- Start
                automatic_sector_max_scanner1 = client.get_node("ns=1;s=AutomaticSector.max")
                automatic_sector_max_temp_scanner1 = automatic_sector_max_scanner1.get_value()

                automatic_sector_max_scanner2 = client.get_node("ns=2;s=AutomaticSector.max")
                automatic_sector_max_temp_scanner2 = automatic_sector_max_scanner2.get_value()

                max_temp = (automatic_sector_max_temp_scanner1 + automatic_sector_max_temp_scanner2) / 2

                max_temp_value = round(max_temp, 2)

                with open(userPath + '/.amns/LiveData/MaxAvgValue.txt', 'a') as f:
                    f.write(str(max_temp_value) + '\n')
                # Avg Max Value -- End
                # -----------------------------------------------------------------------------------------------------------
                # Line Data of Scanner -- Start
                LastLineScanner1 = client.get_node("ns=2;s=LastLine")
                LastLineTempScanner1 = LastLineScanner1.get_value()
                actualFloatArrayDataOfScanner1 = np.array(LastLineTempScanner1)
                roundOffScanner1Value = np.round_(actualFloatArrayDataOfScanner1)
                data = roundOffScanner1Value.tolist()
                # print("data",data)
                removeUnwantedContentS1 = str(data).replace(".0", "").replace('[', '').replace(']', '').replace(',', '')
                # print("LastLineScanner1", len(LastLineScanner1))
                # print("LastLineTempScanner1", removeUnwantedContentS1)
                # print("removeUnwantedContentS1", removeUnwantedContentS1)
                datasave1=self.Convert(removeUnwantedContentS1)

                datasave1convertStringListToInt1 = [int(numeric_string) for numeric_string in np.asarray(datasave1)]

                convertStringToList1 = self.Convert(removeUnwantedContentS1)
                # print("convertStringToList1",len(convertStringToList1))

                configFilePathplc = 'C:/.amns/LiveData/plc_data.txt'
                plcdata = []

                with open(configFilePathplc, "r") as file:
                    f = file.readlines()[-1]
                    plcdata = str(f).split("  ")


                del convertStringToList1[0:1045]
                removeUnwantedData1 = convertStringToList1[:len(convertStringToList1) - 225]
                #removeUnwantedData1 = convertStringToList1
                # print("removeUnwantedData1", removeUnwantedData1)



                thikness1 = removeUnwantedData1[0:5]
                thik1 = [int(numeric_string) for numeric_string in np.asarray(thikness1)]
                thinkness1avg = sum(thik1) / len(thik1)
                sla1 = removeUnwantedData1[5:]
                slap1 = [int(numeric_string) for numeric_string in np.asarray(sla1)]
                slab1avg = sum(slap1) / len(slap1)


                p1=removeUnwantedData1[12]
                p2=removeUnwantedData1[15]
                t1=float(removeUnwantedData1[4])


                convertStringListToInt1 = [int(numeric_string) for numeric_string in np.asarray(removeUnwantedData1)]

                LastLineScanner2 = client.get_node("ns=1;s=LastLine")
                LastLineTempScanner2 = LastLineScanner2.get_value()  # get float array data from line Scanner 1 with decimal
                #print("LastLineTempScanner2",len(LastLineTempScanner2))
                # process start to round off the values from float array
                actualFloatArrayDataOfScanner2 = np.array(LastLineTempScanner2)
                roundOffScanner2Value = np.round_(actualFloatArrayDataOfScanner2)

                data2 = roundOffScanner2Value.tolist()

                removeUnwantedContentS2 = str(data2).replace(".0", "").replace('[', '').replace(']', '').replace(',','')
                #print("removeUnwantedContentS2",removeUnwantedContentS2)
                datasave2 = self.Convert(removeUnwantedContentS2)
                datasave2convertStringListToInt2 = [int(numeric_string) for numeric_string in np.asarray(datasave2)]
                convertStringToList2 = self.Convert(removeUnwantedContentS2)

                del convertStringToList2[0:205]

                removeUnwantedData2 = convertStringToList2[:len(convertStringToList2) - 1058]
                #removeUnwantedData2=convertStringToList2

                thikness2 = removeUnwantedData2[len(removeUnwantedData2) - 6:len(removeUnwantedData2) - 1]
                #thikness2 = removeUnwantedData2[0:9]

                thik2 = [int(numeric_string) for numeric_string in np.asarray(thikness2)]
                thinkness2avg = sum(thik2) / len(thik2)
                sla2 = removeUnwantedData2[0:len(removeUnwantedData2)-6]

                slap2 = [int(numeric_string) for numeric_string in np.asarray(sla2)]
                slab2avg = sum(slap2) / len(slap2)

                p3=removeUnwantedData2[5]
                p4=removeUnwantedData2[10]
                p5=removeUnwantedData2[15]
                t2=float(removeUnwantedData2[len(removeUnwantedData2)-5])

                PLCDBWriteData().WriteData(thinkness1avg, thinkness2avg, slab1avg, slab2avg, p1, p2, p3, p4, p5,t1,t2)
                dictionary = [
                    thinkness1avg,
                    thinkness2avg,
                    slab1avg,
                    slab2avg,
                    float(p1),
                    float(p2),
                    float(p3),
                    float(p4),
                    float(p5),
                    InternalTemperaturescanner1,
                    InternalTemperaturescanner2,
                    t1,
                    t2
                ]

                # Serializing json
                data = str(dictionary).replace('[', '').replace(']', '').replace(',', ' ').replace(',', ' ')
                # print("data", data)
                # Writing to sample.json
                if os.path.exists('C:/.amns/LiveData/caster_data.txt'):
                    fileSize = os.path.getsize('C:/.amns/LiveData/caster_data.txt')
                    if fileSize > 50000000:
                        os.remove('C:/.amns/LiveData/caster_data.txt')
                    else:
                        with open('C:/.amns/LiveData/caster_data.txt', 'a') as f:
                            f.write(data + '\n')
                else:
                    with open('C:/.amns/LiveData/caster_data.txt', 'a') as f:
                        f.write(data + '\n')

                convertStringListToInt2 = [int(numeric_string) for numeric_string in np.asarray(removeUnwantedData2)]
                mergeTwoList = convertStringListToInt1 + convertStringListToInt2
                removeBracket = str(mergeTwoList).replace('[', '').replace(']', '').replace(',', ' ')


                realdatamerge=datasave1convertStringListToInt1+datasave2convertStringListToInt2
                realdataremoveBracket = str(realdatamerge).replace('[', '').replace(']', '').replace(',', ' ')

                if os.path.exists(userPath + '/.amns/LiveData/ThermalLiveData.txt'):
                    fileSize = os.path.getsize(userPath + '/.amns/LiveData/ThermalLiveData.txt')
                    if fileSize > 50000000:
                        os.remove(userPath + '/.amns/LiveData/ThermalLiveData.txt')
                    else:
                        with open(userPath + '/.amns/LiveData/ThermalLiveData.txt', 'a') as f:
                            f.write(removeBracket + '\n')
                else:
                    with open(userPath + '/.amns/LiveData/ThermalLiveData.txt', 'a') as f:
                        f.write(removeBracket + '\n')
                # Line Data of Scanner -- End
                # -----------------------------------------------------------------------------------------------------------
                # Set emissivity of both scanner -- Start
                # set emissivity
                emissivity1 = client.get_node("ns=1;s=Emissivity")
                emissivity2 = client.get_node("ns=2;s=Emissivity")
                emissivity1.set_value(emissivity, VariantType.Float)
                emissivity2.set_value(emissivity, VariantType.Float)

                # Set emissivity of both scanner -- End
                # -----------------------------------------------------------------------------------------------------------
                # # Create Slab on bases of PLC trigger -- Start

                # working code.
                # plc_cut_trigger = True

                fileToSave =plcdata[1].replace(".0", '')
                print("fileToSave",fileToSave)
                print("slabGlobal",slabGlobal)

                if (slabGlobal != plcdata[1]):
                    path = userPath + '/.amns/MergeFiles/Slab_'+slabGlobal.replace(".0", '')+'.txt'
                    realDataPath='C:/Users/Admin/Documents/data/Slab_'+slabGlobal.replace(".0", '')+'.txt'

                    if os.path.exists(path):
                        newfileName = now.strftime("_%d_%m_%Y_%H_%M")
                        newpath = userPath + '/.amns/HeatmapFiles/Slab_'+slabGlobal.replace(".0", '')+newfileName+ '.txt'
                        self.convertTranform(path, newpath)
                        os.remove(path)

                    if os.path.exists(realDataPath):
                        newfileName = now.strftime("_%d_%m_%Y_%H_%M")
                        newrealDataPath = 'C:/Users/Admin/Documents/data_transfer/Slab_' + slabGlobal.replace(".0",'') + newfileName + '.txt'


                        # print('real', realDataPath)
                        # print('newreal', newrealDataPath)
                        self.convertTranform(realDataPath, newrealDataPath)
                        os.remove(realDataPath)
                    slabGlobal = plcdata[1]

                with open(userPath + '/.amns/MergeFiles/Slab_'+ fileToSave+'.txt', 'a') as f:
                    f.write(removeBracket + '\n')


                with open('C:/Users/Admin/Documents/data/Slab_'+ fileToSave+'.txt', 'a') as f:
                    f.write(realdataremoveBracket + '\n')

                with open(userPath + '/.amns/MergeFiles/Slab_S1_S2_' + oneDateFile + '.txt', 'a') as f:
                    f.write(removeBracket + '\n')
        except:
            LoggerData().logger.error("Line Laser loss connection")
            self.getDataFromScanner()

    def convertTranform(self, filepath, newfilepath):

        data = np.loadtxt(filepath, skiprows=1, dtype=int)
        data_T = data.T

        for x in data_T:
            roundOffScanner2Value = x.tolist()
            removeBracket = str(roundOffScanner2Value).replace(",", "").replace('[', '').replace(']', '')
            # print('filepath',filepath)
            with open(newfilepath, 'a') as f:
                f.write(removeBracket + '\n')

    def run(self) -> None:
        linescanner = LineScanner()
        linescanner.getDataFromScanner()
        time.sleep(1)
