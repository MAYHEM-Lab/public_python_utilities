#from: https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/
#Libraries
import Adafruit_DHT as dht
from time import sleep
#Set DATA pin
DHT = 4 #change this if you use a different GPIO pin
while True:
    #Read Temp and Hum from DHT22 or DHT11 (change the args below depending)
    h,t = dht.read_retry(dht.DHT11, DHT)
    #Print Temperature and Humidity on Shell window
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
    sleep(5) #Wait 5 seconds and read again
