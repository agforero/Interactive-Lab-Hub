import paho.mqtt.client as mqtt
import uuid

# the # wildcard means we subscribe to all subtopics of IDD
topic = 'IDD/#'

# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# oled imports
import board
import busio
import qwiic
import time
import adafruit_ssd1306

# oled setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)
oled.show()

# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
        #print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
        if msg.topic == "IDD/imuTest/d1":
            return

        print(repr(msg.topic))
        if msg.topic == "IDD/joe/test/cap":
            oled.fill(1)
            oled.show()
            time.sleep(0.25)
            oled.fill(0)
            oled.show()
        else:
            oled.fill(0)
            oled.show()
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()
