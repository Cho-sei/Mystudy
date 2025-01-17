import serial
import serial.tools.list_ports
import threading
import time
from tqdm import tqdm
import pandas as pd
import sys
import itertools

class Trigger(object):
    def __init__(self, baudrate=57600):
        for com in ['COM' + str(num) for num in range(10)]:
            try:
                self.ser = serial.Serial(com, baudrate)
            except:
                continue
            else:
                print(com)
                trigger_thread(self.ser, b'\x00')
                self.TriggerTable = pd.read_csv('trigger_table.csv', index_col=0)
        
        try:
            self.SendTrigger('start')
        except:
            raise ValueError('error')
    
    def SendTrigger(self, value):
        trigger_onset = threading.Thread(
            target=trigger_thread, args=(self.ser, chr(int(self.TriggerTable.loc[value].trigger)).encode()))
        trigger_onset.start()
    
def trigger_thread(ser, sendValue):
    ser.write(sendValue)
    time.sleep(.05)
    ser.write(b'\x00')


class TestMode(object):
    def __init__(self):
        print('Enter Test Mode')

    def SendTrigger(self, value):
        print('Sent trigger ' + value)

try:
    trigger = Trigger()
except:
    trigger = TestMode()

if __name__ == '__main__':
    trigger.SendTrigger('start')