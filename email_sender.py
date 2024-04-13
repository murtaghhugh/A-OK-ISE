#all imports managed at the top of the file

#allows code to read when the button is pressed via signal through specified pins
import RPi.GPIO as GPIO

#allows code to check whether files exist and to remove files
#used to check if "a_ok_data.csv" exists so as to decide whether or not to execute code avoiding errors
import os 

#checking time of day for classes and preventing re-execution of code within a certain amount of time
from datetime import datetime
import time

#used to format message for gmail and to send the emails
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

now = datetime.now()

#message is declared with formatable spaces for teacher name and email
base_message = """Hi {name}!

Hugh is quite stressed out. If you 
could excuse him from {my_class} class that 
would be greatly appreciated.
Thanks very much.
Have a nice day!

Mike
A-Ok team

"""

#declares function to be executed if file exists
def email_sender():
    #declares list of classes
    student_classes = []
    f= open("/home/pi/Desktop/rasberry_pi_files/a_ok_data.csv","r")
    #loops through each line in the file
    for line in f:
        #splits each line by comma and space making a list
        student_class = line.split(",")
        #loops through each item in the line and removes any extra spaces either side
        for i in range(0, len(student_class)):
            student_class[i] = student_class[i].strip()
        #appends class data in list format to student_classes
        student_classes.append(student_class)
    #closes file    
    f.close()

    #uses datetime to set a variable equal to todays day
    day = now.strftime("%a")

    day_classes = []
    #loops through the  list of classes and appends any classes on todays day to a list
    for i in student_classes:
        if i[0].lower().strip() == day.lower().strip():
            day_classes.append(i)

    #sets a variable equal to the current time hours and minutes
    current_time = now.strftime("%H: %M")
    #declares a variable for todays class
    current_class = "No class"
    #loops through first four possible days this as they all have the same number of classes
    if day_classes[0][0] in ["mon", "tue", "wed", "thur"]:
        #checks for each class time to see if it is currently that time
        #if so sets that class to the current class variable
        if str(current_time[0:2]) == "09":
            current_class = day_classes[0]
        elif str(current_time[0:2]) == "10":
            current_class = day_classes[1]
        elif str(current_time[0:2]) == "11":
            if int(current_time[4:6]) >= 15:
                current_class = day_classes[2]
        elif str(current_time[0:2]) == "12":
            if int(current_time[4:6]) < 15:
                current_class = day_classes[2]
            else:
                current_class = day_classes[3]
        elif str(current_time[0:2]) == "13":
            if int(current_time[4:6]) < 15:
                current_class = day_classes[3]
        elif str(current_time[0:2]) == "14":
            current_class = day_classes[4]
        elif str(current_time[0:2]) == "15":
            current_class = day_classes[5]
        else:
            quit

    #does the same for fridays four classes
    elif day_classes[0][0] == "fri":
        if str(current_time[0:2]) == "09":
            current_class = day_classes[0]
        elif str(current_time[0:2]) == "10":
            current_class = day_classes[1]
        elif str(current_time[0:2]) == "11":
            if int(current_time[4:6]) >= 15:
                current_class = day_classes[2]
        elif str(current_time[0:2]) == "12":
            if int(current_time[4:6]) < 15:
                current_class = day_classes[2]
            else:
                current_class = day_classes[3]
        elif str(current_time[0:2]) == "13":
            if int(current_time[4:6]) < 15:
                current_class = day_classes[3]
        else:
            quit

    #sets both formatting variables from the current class
    name = str(current_class[2])
    my_class = str(current_class[1])
    finished_msg = base_message.format(
            name = name,
            my_class = my_class,
        )

    #sets login info for sender email
    username = "a.o.k.assistanceteam@gmail.com"
    password  = "Teamaok123"
    #sets receiver email from current class
    #sets their message
    user_email = current_class[3]
    user_msg = finished_msg

    #uses try block to run email sending code
    #this helps avoid errors crashing the code
    try:
        my_context = ssl.create_default_context()
        the_msg = MIMEMultipart("alternative")
        the_msg["Subject"] = "Stressed Out Student"
        the_msg["From"] = username
        the_msg["To"] = user_email
        right_msg = MIMEText(user_msg, "plain")
        the_msg.attach(right_msg)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = my_context) as server:
            server.login(username, password)
            server.sendmail(
                username, user_email, the_msg.as_string()
            )
        print("Email sent")
    except smtplib.SMTPException:
        print("Error sending message")
    except smtplib.SMTPAuthenticationError:
        print("An error occured during login")
        return True
    return False

#function used to decide whether or not to attempt code based on whether or not data file exists
def file_exist():
    #using os module it checks if the file location exists
    #if so it calls email sending function
    if os.path.exists("/home/pi/Desktop/rasberry_pi_files/a_ok_data.csv"):
        email_sender()
    #else tells the user to make a timetable using the timetable making file
    else:
        print("\nPlease make a timetable using the \"data_setup.py\" file\nThen try again")

#sets up pin inputs on rasberry pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#creates infinite loop checking whether the voltage on the pin is high i.e. whether or not the button is pressed
#if so runs "file_exist()" and sets a 2 and half minute programme sleep to prevent email spamming
while True:
    if GPIO.input(10) == GPIO.HIGH:
        file_exist()
        time.sleep(150)