import time
import board
import busio
import adafruit_mpr121

import paho.mqtt.client as mqtt
import uuid

def main():
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)

    topic = 'IDD/security/monitor'

    #i2c = busio.I2C(board.SCL, board.SDA)

    #mpr121 = adafruit_mpr121.MPR121(i2c)

    import qwiic
    from datetime import datetime

    ToF = qwiic.QwiicVL53L1X()
    if (ToF.sensor_init() == None):
        print("Sensor online!")

    baseDist = 0.0
    while True:
        ToF.start_ranging()
        time.sleep(0.005)
        distance = ToF.get_distance()
        time.sleep(0.005)

        current_time = datetime.now().strftime("%H:%M:%S")

        if baseDist == 0.0:
            baseDist = distance

        if abs(distance - baseDist) > (0.3 * baseDist):
            warning = f"Intruder detected at {current_time}!"
            print(warning)
            client.publish(topic, warning)

        #client.publish(topic, val)
        time.sleep(0.25)

main()
