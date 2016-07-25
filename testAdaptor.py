'''
Created on Jul 9, 2016

@author: tarunnvdia@gmail.com, TARUN NAVADIA
'''
import json
import logging
import math
import random
import sys
import time
import os
import ZigBeeAdaptor
import binascii

from com.altizon.aliot import *

def my_instruction_handler(gateway, timestamp, thing_key, alert_key, instruction):
    logging.info('Successfully handled incoming instruction: ' + json.dumps(instruction))
    if gateway.instruction_ack(alert_key, 'Successfully handled instruction', 1, {'execution_status':'success'}):
        logging.info('Sent instruction execution ACK back to datonis')
    else:
        logging.warn('Could not send instruction execution ACK back to datonis')
    

def send_example_alert(gateway, thing, alert_level, alert_level_str):
    if gateway.alert(thing.thing_key, 'This is an example ' + alert_level_str + ' alert using python SDK', alert_level, {'foo':'bar'}) == True:
        logging.info('Successfully sent ' + alert_level_str + ' alert to datonis')
    else:
        logging.warn('Failed to send ' + alert_level_str + ' alert to datonis')
    

def send_example_alerts(gateway, thing):
    send_example_alert(gateway, thing, 0, 'INFO')
    send_example_alert(gateway, thing, 1, 'WARNING')
    send_example_alert(gateway, thing, 2, 'ERROR')
    send_example_alert(gateway, thing, 3, 'CRITICAL')

def main():
    newZigBeeAdaptor = ZigBeeAdaptor.ZigBeeAdaptor()
    logging.basicConfig(filename='aliot-agent.log', level = logging.INFO, format = '%(asctime)s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Starting aliot agent')
    
    ###################################################### USE ONE OF THE 4 OPTIONS below to create a gateway ###############################################
    # NOTE: If you intend to use MQTT mode, then multi-threading support is required and assumed
    
    # Connect over MQTTs
    # gateway_config = GatewayConfig('1d2fb5c369863fd54afafde654c26dtd51122t8e', 'f4e31122629etaeaa48d9c8c72b8cctfc9d63acc', 'mqtts', '/data/play/chain.pem')
    
    # Connect over MQTT
    # gateway_config = GatewayConfig('1d2fb5c369863fd54afafde654c26dtd51122t8e', 'f4e31122629etaeaa48d9c8c72b8cctfc9d63acc', 'mqtt')
    
    # Connect over HTTP
    gateway_config = GatewayConfig('89891tb9116tf1df958223e1c78a8252fd6dd18t', '2fc671ff31c92785b2ef29ddaacf9c4b8412fa9f', 'http')

    #access_key: 89891tb9116tf1df958223e1c78a8252fd6dd18t
    #secret_key: 2fc671ff31c92785b2ef29ddaacf9c4b8412fa9f

    
    # Connect over HTTPs
    # gateway_config = GatewayConfig('1d2fb5c369863fd54afafde654c26dtd51122t8e', 'f4e31122629etaeaa48d9c8c72b8cctfc9d63acc', 'https')
    
    #############################################################################################################################################################
    
    gateway = gateway_config.create_gateway()
        
    if gateway.connect() == False:
        logging.error("Failed to connect to Datonis")
    else:
        logging.info("Successfully connected to Datonis")
    
    thing = Thing()
    #thing.thing_key = 'a21e47c9a2'
    thing.thing_key = '' #insert your key here
    thing.name = 'LeakageDetection1'
    
    # Uncomment lines below if you are using MQTT/MQTTs and require instruction execution support
    # thing.bi_directional = True
    # gateway.instruction_handler = my_instruction_handler
    
    if gateway.thing_register(thing) == False:
        logging.error("Failed to register thing")
        sys.exit(1)
    else:
        logging.info("Registered thing: " + thing.name + " with metadata: " + str(thing.data))
        
    if True:
        send_example_alerts(gateway, thing)
        
    counter = -1
    data_prev = (binascii.hexlify(newZigBeeAdaptor.read()['rf_data']))
    while True:
        
        counter = (counter + 1) % 5
        if counter == 0:
            if gateway.thing_heartbeat(thing) == False:
                logging.warn("Could not send hearbeat for thing: " + thing.name)
            else:
                logging.info("Heartbeat sent for thing: " + thing.name)
                
        #data = {'temperature': math.ceil(random.uniform(0, 100)), 'humidity': math.ceil(random.uniform(0, 100))}
        #data = {'FlowRate': math.ceil(random.uniform(0, 100))}
        #print(binascii.hexlify(newZigBeeAdaptor.read()['rf_data']))
        data_now = (binascii.hexlify(newZigBeeAdaptor.read()['rf_data']))      
        speed = (int(data_now) - int(data_prev))
        data_prev = data_now
        sim_high = int(1*(speed))
        sim_low = int(0.8*(speed))
        data = {'CurrentFlowRate':speed,'SimulatedFlowRate':random.uniform(sim_low,sim_high)}
        print(speed)
        
        thing.description = None
        waypoint = [18.5158, 73.9272]
        #waypoint format: [latitude, longitude]
        
        thing_event = aliot_util.create_thing_event(thing, data, waypoint)
        
        #Simulating the new thing here
        
        #data_sim = {'SimulatedFlowRate':speed-3}
        #thing_event = aliot_util.create_thing_event(thing, data_sim, waypoint)
        
        
        
        
        #pass data as None to send only waypoint.
        #pass waypoint as None to send only data.
        #or pass both data and waypoint to send both of them.
        #you can also send timestamp as fourth parameter to create_thing_event, default it will send current time.
        #thing_event = aliot_util.create_thing_event(thing, data)
        #thing_event = aliot_util.create_thing_event(thing, None, waypoint)
        #thing_event = aliot_util.create_thing_event(thing, data, waypoint)
        #thing_event = aliot_util.create_thing_event(thing, data, None, int(time.time()*1000))
        if gateway.thing_event(thing_event) == True:
            logging.error("Sent event data for thing: " + str(thing_event))
        else:
            logging.error("Failed to send event data for thing: " + str(thing_event))
        #time.sleep(30)
    logging.info('Exiting aliot agent')

main()