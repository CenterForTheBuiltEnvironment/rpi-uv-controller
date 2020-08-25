import time  
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)  

touchSwitch = 5
outputPin = 24  

GPIO.setup(touchSwitch, GPIO.IN)
GPIO.setup(outputPin, GPIO.OUT)  
GPIO.output(outputPin, False)  

while True:  
    switchTouched = GPIO.input(touchSwitch)  

    if switchTouched:  
        print ("touch detected")
        time.sleep(0.3) # sleep again here so not to toggle the lamp to quickly  
    else:  
        print ("not touched")

    time.sleep(0.15) # 0.10 seems to give the best results but 0.15 uses less CPU 