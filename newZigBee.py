import xbee
import time
import serial
import pprint
import binascii
import Class_waterflow

"""
class ZigBee():


    def send(self,xbee1):

"""
if __name__ == '__main__' :

    PORT = '/dev/ttyUSB0'
    #PORT = 'COM3'
    BAUD = 9600

    ser = serial.Serial(PORT, BAUD)
    xbee1 = xbee.zigbee.ZigBee(ser)
    newFlowSensor = Class_waterflow.FlowSensor()
    scale=newFlowSensor.lenCal()
    data_prev=scale
    time_prev = time.time()


    #newZigBee = ZigBee()
    #newZigBee.send(xbee1)
    while True:
        try:

            scale=newFlowSensor.lenCal()
            print(scale)
            data_now=scale

            #send = (binascii.unhexlify(data_send.zfill(8)))
            #print(send)
            #data_now= f.read()

            if (data_now - data_prev)< 200:
                pass
            else:
                if (time.time()-time_prev)>5:
                    send = (binascii.unhexlify(str(data_now).zfill(8)))
                    print(send)

                    xbee1.tx_explicit(frame_id='\x01',dest_addr_long='\x00\x13\xA2\x00\x40\xBD\xB5\xA0', src_endpoint='\xE8',dest_endpoint='\xE8',
                              broadcast_radius='\x00', profile='\xC1\x05',data=send,cluster='\x00\x11',options='\x01',dest_addr='\x00\x00')
                    pprint.pprint(xbee1.wait_read_frame())
                    print('Successfully sent the packet')
                    data_prev = data_now
                    time_prev = time.time()

        except KeyboardInterrupt:
            print '\ncaught keyboard interrupt!, bye'
            GPIO.cleanup()
            sys.exit()
