
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
#from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys

# oled imports
import board
import busio
import qwiic
import adafruit_ssd1306

# oled setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.show()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      #print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      #print("Unable to access webcam.")
      pass


# Load the model
model = tensorflow.keras.models.load_model("emotion_model/keras_model.h5")
#model = load_model("emotion_model/keras_model.h5")

# Load Labels:
labels=[]
f = open("emotion_model/labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())


print("Script successfully initialized. Beginning to monitor feelings.")
while(True):
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)

    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    
    #print("I think its a:",labels[np.argmax(prediction)])

    with open("output.txt", 'r') as f:
        raw = f.read().split()
        numer, denom = int(raw[0]), int(raw[1])

    # recording to records.txt
    if labels[np.argmax(prediction)] == "Happy":
        oled.fill(1)

        numer += 1
        denom += 1
        with open("output.txt", 'w') as f:
            f.write(f"{numer}\n{denom}")

    else:
        oled.fill(0)

        denom += 1
        with open("output.txt", 'w') as f:
            f.write(f"{numer}\n{denom}")

    oled.show()

    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        #cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
