import simple as mqtt
import network
import time    
import controller as gamepad
import urequests as requests



global lastsent1
lastsent1= "stopped"
global lastsent2
lastsent2= "stopped"
global sending
sending = "stopped"


station = network.WLAN(network.STA_IF)
station.active(True)

station.connect('Tufts_Wireless')
while station.isconnected() == False:
    time.sleep(1)
    pass
print('Connection successful')
print(station.ifconfig())

YOUR_USERNAME = 'Jberke327'  # Replace with your Adafruit IO username
YOUR_AIOKEY = 'aio_SUOq77frYgPzWYbHJjWm4tbK0SkF'  # Replace with your Adafruit IO AIO key

url = f'https://io.adafruit.com/api/v2/{YOUR_USERNAME}/feeds'  # Use an f-string to insert your username

headers = {'X-AIO-Key': YOUR_AIOKEY, 'Content-Type': 'application/json'}

reply = requests.get(url, headers=headers)

if reply.status_code == 200:
    print(reply.text)
    reply_data = reply.json()  # Parse the JSON response into a Python data structure
    keys = [x['key'] for x in reply_data]
    groups = [x['group']['name'] for x in reply_data]
    names = [x['name'] for x in reply_data]
    values = [x['last_value'] for x in reply_data]
    ids = [x['id'] for x in reply_data]
    print(keys)
    print(values)
else:
    print(f"Request failed with status code: {reply.status_code}")
 
#/opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf to start
# mosquitto_sub -t 'JordanandShiv' -h 10.243.51.89 -p 1883 to sub
        

def send():
    broker = '10.243.51.89' #change this as needed
    ssid = 'Tufts_Wireless'
    password = ''
    topic_pub = "JordanandShiv" #publishing to this topic 
    #topic_sub = "Pico/listen" #in case 2-way communication, subscribe to the topic that the other device is publishing to
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print("Connected to WiFi")
    #print(wlan.ifconfig()) #this is supposed to get my IP Address...doesn't work idk

    def whenCalled(topic, msg):
        print((topic.decode(), msg.decode()))

    fred = mqtt.MQTTClient('BoneSend', broker, keepalive=600)
    fred.connect()

    print("Sending")
    gamepad.digital_setup()
    while True: #send out gamepad values to the other pico
        sending = ""
        fred.check_msg()
        x, y, button = gamepad.read_everything()
        if y > 1000:
            sending = "forward"
            publish1(sending)
        elif y < 400:
            sending = "back"
            publish1(sending)
        
        elif x > 700:
            sending = "right"
            publish1(sending)
        
        elif x < 400:
            sending = 'left'
            publish1(sending)
        
        elif button == 'A':
            sending = 'lowerright'
        elif button == 'Y':
            sending = 'lowerleft'
        elif button == 'X':
            sending = 'upperup'
            publish2(sending)
        
        elif button == 'B':
            sending = 'upperdown'
            publish2(sending)
        
        else:
            sending = "stopped"
            publish1(sending)
            publish2(sending)
        
        
        fred.publish(topic_pub, sending)
        print(sending)
        time.sleep(0.01)
        
def publish1(message):
    global lastsent1
    if (lastsent1 != message):
        url = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (YOUR_USERNAME, "forward")
        data = {'value':message}
        reply = requests.post(url,headers=headers,json=data)
        reply.close()
    else:
        lastsent1 = message

def publish2(message):
    global lastsent2
    if (lastsent2 != message):
        url = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (YOUR_USERNAME, "up-down")
        data = {'value':message}
        reply = requests.post(url,headers=headers,json=data)
        reply.close()
    else:
        lastsent2 = message

send()