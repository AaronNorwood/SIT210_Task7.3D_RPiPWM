import RPi.GPIO as GPIO
import time

LED = 21
##using the pin names rather than the numbers
GPIO.setmode(GPIO.BCM)
##configure the LED and pwm
GPIO.setup(LED, GPIO.OUT)   
pwm = GPIO.PWM(LED, 100)    
pwm.start(0) 
 
#set the pins for the hc-sr04
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    #declare the variables we're going to need
    StartTime = time.time()
    StopTime = time.time()
 
    #get the time the measurement started
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    #time the signal returned
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    #get the difference between the signal being send and returning
    TimeElapsed = StopTime - StartTime
    #multiplying by the speed the signal travels at (34300cm/s)
    #divide by two since it need to travel out then return
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            #get the distance from nearest object
            dist = distance()
            #maps the duty cycle from a high value to a low value
            #and vice versa
            dutyCycle = 400 / dist
            #prevents duty cycle exceeding 100 since that throws an error
            if(dutyCycle > 100):
                dutyCycle = 100
            #print out values and set duty cycle
            print("Duty cycle is %1f:"% dutyCycle)
            pwm.ChangeDutyCycle(dutyCycle)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
    except KeyboardInterrupt:
        print("Program ended by keyboard interrupt ")
        pwm.stop() 
        GPIO.cleanup()

