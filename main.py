API_KEY = "" #This is  the API key for the Bolt device used by me
DEVICE_ID = "BOLTXXXXXXXX" #This is the Bolt Device ID used by me
SID = "" #Twilio SID signed up to send sms alerts
AUTH_TOKEN = "" #Twilio Authorised Token to verify the phone number
FROM_NUM = "" #The Twilio Number from where the sms alert will be generated
TO_NUM = "" #The personal number to receive the sms alert

from boltiot import Bolt , Sms
import time , json , sys , statistics
R = 5
C = 5
data_set = []
alarm_state = 0

mybolt = Bolt(API_KEY,DEVICE_ID) #importing bolt api key and devide id from conf.py
sms = Sms(SID,AUTH_TOKEN,TO_NUM,FROM_NUM)# importing twillo sid , auth ,and numbers

def check_device(): #function for checking the device 
        data = json.loads(mybolt.isOnline())
        if data["value"]=="online":
                print('Device online')
                mybolt.digitalWrite("1","HIGH")
        else:
                print('Device offline.')
                sys.exit()

def get_temp(): #function for getting temp values
        data = json.loads(mybolt.analogRead("A0"))
        if data["success"]==1:
                val =float(data["value"])
                temp =  100 * val / 1024
                return temp

        else:
                return -999

def set_limits(data_set,R,C): #function for performing z-score analysis
        if len(data_set)<R:
                return None
        if len(data_set)>R:
                data_set=data_set[len(data_set)-R:]

        Mean = statistics.mean(data_set)
        Variance = 0
        for data in data_set:
                Variance += (data - Mean) ** 2
        Zn = C * ((Variance / R) ** 0.5)
        H = data_set[R-1] + Zn
        return H

def run_alarm(val): #function for buzzer and sms
        print('Fire possibility High. Turning on Buzzer.')
        sms.send_sms('Sudden raise in temperature. The temperature is '+str(val))
        mybolt.digitalWrite('0','HIGH')
        global alarm_state
        alarm_state = 1

def stop_alarm(val):
                mybolt.digitalWrite('0','LOW')

check_device()

while 1: #indefinite loop for countinous tracking of temparature
        try:
                temp = get_temp()
                print('The temperature is ',temp)
                
                limit = set_limits(data_set,R,C)
                if not limit:
                        print('Not enough values to conduct Z-score analysis. More values required.')
                        data_set.append(temp)
                else:
                        if temp > limit:
                                run_alarm(temp)
                        else:
                                if alarm_state:
                                        stop_alarm(temp)
                                        alarm_state = 0
                        data_set.append(temp)

                time.sleep(10)

        except KeyboardInterrupt: #press ctrlc + c for stopping the loop
                print('Device Stopped.')
                mybolt.digitalWrite('1','LOW')
                mybolt.digitalWrite('0','LOW')
                sys.exit()
 