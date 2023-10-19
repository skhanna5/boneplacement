import machine
from machine import Pin, PWM
import simple as mqtt
import network
import time

#initialize car motors
rmotor=PWM(Pin(15))
lmotor=PWM(Pin(12))
#initialize arm motors
lowerarm=PWM(Pin(13))
upperarm=PWM(Pin(0))
motors = [rmotor, lmotor, lowerarm, upperarm]
for motor in motors:
    motor.freq(200)
back1 = Pin(14, machine.Pin.OUT)
back2 = Pin(17, machine.Pin.OUT)
front1 = Pin(1, machine.Pin.OUT)
front2 = Pin(27, machine.Pin.OUT)

broker = '10.243.51.89' #change this as needed
ssid = 'Tufts_Wireless'
password = ''
topic_pub = 'JordanandShiv' #publishing to this topic
#topic_sub = “Pico/listen” #in case 2-way communication, subscribe to the topic that the other device is publishing to
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print('Connected to WiFi')
fred = mqtt.MQTTClient('BoneRecieve', broker, keepalive=600)
fred.connect()
print('Connected and Subscribed')
x = ''

def main():
    def whenCalled(topic, msg):
        global x
        print (f"topic {topic} received message {msg}")
        x = msg.decode()
        time.sleep(0.01)
    while True: #listen for sent inputs and output to motor accordingly
        fred.set_callback(whenCalled)
        fred.subscribe(topic_pub) #subscribe to whatever topic you want to listen to
        fred.check_msg()
        if x == "forward":
            # print('forward')
            rmotor.duty_ns(1000000)
            lmotor.duty_ns(2000000)
            back1.value(0)
            back2.value(0)
            front1.value(1)
            front2.value(1)
        elif x == "back":
            # print('back')
            rmotor.duty_ns(2000000)
            lmotor.duty_ns(1000000)
            back1.value(0)
            back2.value(0)
            front1.value(0)
            front2.value(0)
        elif x == "right":
            # print ('right')
            rmotor.duty_ns(0)
            lmotor.duty_ns(2000000)
            back1.value(0)
            back2.value(0)
            front1.value(0)
            front2.value(1)
        elif x == "left":
            # print ("left")
            rmotor.duty_ns(1000000)
            lmotor.duty_ns(0)
            back1.value(0)
            back2.value(0)
            front1.value(1)
            front2.value(0)
        elif x == "stopped":
            # print ("stopped")
            rmotor.duty_ns(0)
            lmotor.duty_ns(0)
            upperarm.duty_ns(0)
            lowerarm.duty_ns(0)
            back1.value(1)
            back2.value(1)
            front1.value(0)
            front2.value(0)
        elif x == "lowerright":
            lowerarm.duty_ns(1000000)
            upperarm.duty_ns(0)
        elif x == "lowerleft":
            lowerarm.duty_ns(2000000)
            upperarm.duty_ns(0)
        elif x == "upperdown":
            lowerarm.duty_ns(0)
            upperarm.duty_ns(1000000)
        elif x == "upperup":
            lowerarm.duty_ns(0)
            upperarm.duty_ns(2000000)
        time.sleep(0.01)

main()