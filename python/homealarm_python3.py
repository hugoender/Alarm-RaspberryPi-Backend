# Import webiopi for browser interface
import webiopi

# Import smtplib to provide email functions
import smtplib

# Import urllib so that we can retrieve foscam image
import urllib.request, urllib.parse, urllib.error

# Import date and time
import datetime

# Import time in order to set a delay interval
import time

# Import the email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage 

# Import RPi.GPIO to provide GPIO functions
import RPi.GPIO as GPIO

#--------------------------------------------------
# Use GPIO header numbers not Broadcomm pin numbers
GPIO.setmode(GPIO.BOARD)

# Set up the GPIO variables
alarm_siren=##

GPIO.setup(alarm_siren, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#--------------------------------------------------
# Ask user what phone number to send text to and what message to include
#phone_number = raw_input('What number do you want to send text to? ')
#message = raw_input('What do you want to send them? ')

# Define email addresses to use
#addr_to = '%s@mms.att.net' % phone_number.split(',')
addr_to = '##########@mms.att.net,EmailAddress@gmail.com'
addr_from = 'Raspberry Pi'

# Define SMTP email server details
smtp_server = 'smtp.gmail.com'
smtp_port   = 587
smtp_user   = 'EmailAddress@gmail.com'
smtp_pass   = 'Password'

#--------------------------------------------------
# Define callback function so that a thread is run to immediately respond to a
# change in GPIO status even while program is running
def send_notification(channel):
	# Capture foscam camera images and save them locally
	urllib.request.urlretrieve("http://10.10.10.1:1234/snapshot.cgi?user=UserName&pwd=Password&resolution=32", "FileName.jpg")
	urllib.request.urlretrieve("http://10.10.10.1:1234/snapshot.cgi?user=UserName&pwd=Password&resolution=32", "FileName.jpg")
	
	# Get date and time and add it to the text message
	now = datetime.datetime.now().strftime('%B-%d-%Y %H:%M')

	# Create msg
	msg = MIMEMultipart()
	msg['To'] = addr_to
	msg['From'] = 'EmailAddress@gmail.com'
	# Text component of the message
	msgText = MIMEText('HOME ALARM!<br>Activated:<br>%s<br>Police:(###) ###-####' % now, 'html')
	msg.attach(msgText)

	# Open the image files, attach them, and then close the images
	image1 = "FileName.jpg"
	image2 = "FileName.jpg"

	file1 = open(image1, 'rb')
	file2 = open(image2, 'rb')
	
	attachment1 = MIMEImage(file1.read())
	attachment2 = MIMEImage(file2.read())

	file1.close()
	file2.close()

	attachment1.add_header('Content-Disposition','attachment',filename=image1)
	attachment2.add_header('Content-Disposition','attachment',filename=image2)

	msg.attach(attachment1)
	msg.attach(attachment2)

	# Send the message via an SMTP server
	smtpserver = smtplib.SMTP(smtp_server,smtp_port)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(smtp_user,smtp_pass)
	smtpserver.sendmail(addr_from, addr_to.split(","), msg.as_string())
	smtpserver.quit()
	
	#conn.send('sendtext')
	
	print('Sent text on %s' % now)
	
	# Add a delay between texts
	time.sleep(10)

def check_validity(channel):
	GPIO_count = 0
	alarm_timer_msec = 1000 
	
	while alarm_timer_msec > 0:
		if GPIO.input(channel) == GPIO.LOW:
			GPIO_count = GPIO_count + 1
		
		time.sleep(0.2)
		
		alarm_timer_msec = alarm_timer_msec - 200
		
	if GPIO_count > 4:
		send_notification(alarm_siren)
	
GPIO.add_event_detect(alarm_siren, GPIO.FALLING, callback=check_validity, bouncetime=1000)
