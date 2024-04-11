from twilio.rest import Client
import winsound
import pyttsx3
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

# Define a function to speak out the warning message
def speak_warning(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


# Define a function to play an alarm sound
def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 2000  # Set Duration To 2000 ms == 2 seconds
    winsound.Beep(frequency, duration)


# Define a function to send SMS using Twilio
def send_sms(alert_type):
    account_sid = ""
    auth_token = ""
    twilio_number = ""
    target_number = ""
    
    client = Client(account_sid, auth_token)
    if alert_type == 'fire':
        message_body = f"{timestamp}:Fire detected! This is a notification from your Protected Environment System . Please contact your nearby fire brigade."
    elif alert_type == 'weapon':
        message_body = f"{timestamp}: Weapon detected! This is a notification from your Protected Environment System . Please take necessary precautions."
    elif alert_type == 'Double':
        message_body = f"{timestamp}: Fire and Weapon detected! This is a notification from your Protected Environment System . Please take necessary precautions."

    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=target_number,
    )
    return message.body