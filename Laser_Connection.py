from opcua import Client
from opcua.ua import VariantType
import json
import time

# import the threading module
from threading import Thread

from loggerFile import LoggerData


class LaserMainCode(Thread):

    def laserData(self):
        try:
            while True:
            # Reading Config data from Config File -- Starting
                configFilePath = 'C:\.amns\AMNSConfigFiles\ConfigFiles\Config.json'
                f = open(configFilePath)
                data = json.load(f)
                url = data['opcua']
                client = Client("opc.tcp://192.168.42.100:4840/")
                client.connect()
                #print("OCP-UA Connected")
                print("[WARNING] Please, do not close this Command Prompt Window, Data fetching is in process from Line Scanner !!")


                laserFilePath = 'C:\.amns\AMNSConfigFiles\ConfigFiles\LaserStatus.json'
                f = open(laserFilePath)
                data = json.load(f)
                status = data['status']



                value = status
                count = 1
                if(value==1):
                    while True:
                        print(count)
                        if(count<15):
                            laser1 = client.get_node("ns=1;s=Laser")  # 30
                            laser2 = client.get_node("ns=2;s=Laser")  # 31
                            laser1.set_value(value, VariantType.Boolean)
                            laser2.set_value(value, VariantType.Boolean)
                            count = count + 1
                        else:
                            laser1 = client.get_node("ns=1;s=Laser")  # 30
                            laser2 = client.get_node("ns=2;s=Laser")  # 31
                            laser1.set_value(0, VariantType.Boolean)
                            laser2.set_value(0, VariantType.Boolean)
                            data['status'] = 0
                            a_file = open("C:\.amns\AMNSConfigFiles\ConfigFiles\LaserStatus.json", "w")
                            json.dump(data, a_file)
                            a_file.close()
                            count=0

                            break



                        time.sleep(60)

                client.disconnect()
                time.sleep(1)
        except:
            LoggerData().logger.error("Laser loss connection")
            self.laserData()

    def run(self) -> None:
        linecode = LaserMainCode()
        linecode.laserData()
        time.sleep(1)