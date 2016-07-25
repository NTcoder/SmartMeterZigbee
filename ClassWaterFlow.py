import time
import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)


class FlowSensor:

    def __init__(self):
        print ("3")
        time.sleep(1)
        print ("2")
        time.sleep(1)
        print ("1")
        time.sleep(1)
        print("blow")
        time.sleep(1)


        #self.d_all=[]
        #self.c1=0
        #self.scale=0
        self.count = 0

        #previus_scale = 0

    def dataCollector (self):
        i=1

        current=[]

        while i<1500:


            self.s=GPIO.input(18)
            current.append(self.s)
            #print (s)
            time.sleep(0.00005)
            i=i+1
            #print(i)


        #print current
        return (current)

    def lenCal(self):
        'this fuction is used to calcuate wind speed'
        c=self.dataCollector()
        #print (c)
        #print (len(c))
        i=0
        for i in range(0,len(c)-1):
            #print("inside")
            e=(c[i+1]-c[i])
            global c1
            global count
            #spd_prev_count = count
            #global d_all
            if e!=0:
                self.count=self.count+1
                print(self.count)
                """
                if self.c1==0:
                    self.c1=i

                else:
                    d=i-self.c1
                    self.d_all.append(d)
                    self.c1=0
                    d=0
                """
            else:
                pass
        return (self.count)

if __name__ == '__main__':

    newFlowSensor = FlowSensor()
    scale=newFlowSensor.lenCal()
    while True:

            try:
                newFlowSensor.d_all=[]
                newFlowSensor.c1=0
                scale=newFlowSensor.lenCal()
                #scale=waterCount()
                print(scale)

            except KeyboardInterrupt:
                print '\ncaught keyboard interrupt!, bye'
                GPIO.cleanup()
                sys.exit()

