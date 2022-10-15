# fire_alarm
Code for the fire alarm system 

The code works with a fire alarm circuit built with the help of Bolt WiFi Module, Buzzer and 2 LEDs.
Also, one needs a free Twilio account, to get a free number, via which the WiFi module will send the user the SMS to its registered mobile number.

The code uses Z-Score Analysis to monitor the temperature in the room via the LM35 sensor. The Z-Score Analysis will constantly be calculating the mean and the variance
from the constantly entering temperature values which is uploaded to the cloud every 10 seconds.

The Z-Score Analysis creates a dynamic threshold for temperature in the room. In case of an outlier, that is, in case of an anomaly, a really high temperature, the 
threshold get crossed. Under that scenario, the buzzer gets turned on, and a SMS alert is sent to the registered mobile number of the user.
