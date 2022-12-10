# Usage

## Test program 1: instructables.py
This is from [instructables.com](https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/)
- This program hardcodes the pin number (DHT = 4)

`python3 instructables.py`

output:
```
Temp=22.9*C  Humidity=84.6%
Temp=22.9*C  Humidity=84.5%
...
```
Press Ctrl-C to quit

## Test program 2: getDHT22TempHumidity.py
This is a modified version of an example from [Adafruit](https://github.com/adafruit/Adafruit_Python_DHT.git)

`python3 getDHT22TempHumidity.py 2304 4`

output (TempF:Hum%):
`73.22:84.50`

This also works:
`python3 getDHT22TempHumidity.py`, and uses pin 17 and assumes 2304 as the device.

Specify a DHT11 (11) or DHT22 (22 - selected here) instead, here with pin 4:
`python3 getDHT22TempHumidity.py 22 4`
