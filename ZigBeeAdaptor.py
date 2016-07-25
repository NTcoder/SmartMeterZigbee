'''
Created on Jul 10, 2016

@author: tarunnvdia@gmail.com    TARUN NAVADIA
'''
import xbee
import time
import pprint
import serial


class ZigBeeAdaptor:
    '''
    Contains the list of Responses and Requests which are sent from ZigBee Sensor
    '''

    
    def __init__(self):
        '''
        None
        '''
        #self.PORT = '/dev/ttyUSB0' #for Linux/Raspberry Pi
        self.PORT = 'COM3'
        self.BAUD = 9600
        ser = serial.Serial(self.PORT, self.BAUD)
        self.xbee1 = xbee.zigbee.ZigBee(ser)
        
    def read(self):
        #pprint.pprint(self.xbee1.wait_read_frame())
        return self.xbee1.wait_read_frame()

if __name__ == '__main__':
    newZigBeeAdaptor = ZigBeeAdaptor()
    while True:
        newZigBeeAdaptor.read()
    
    
    