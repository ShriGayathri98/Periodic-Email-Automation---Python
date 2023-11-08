import smtplib
import email.message
import schedule
import time
import re

server = smtplib.SMTP('smtp.gmail.com:587')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def checkEmail(email):
    if re.search(regex, email):
        return True
    else:
        return False


class PyEmailer(object):
    """
    Class to send email using python

    methods:
        sendEmail: Send email to list of email id

    """
    def __init__(self, your_email_id, your_app_password):
        self.your_email_id = your_email_id
        self.your_app_password = your_app_password

    def sendEmail(self, email_subject: str,
                  email_content: str, listOfEmail: list) -> dict:

        output = {'success': 0, 'failed': 0, 'invalid': 0}

        msg = email.message.Message()
        msg['Subject'] = email_subject
        msg['From'] = self.your_email_id
        password = self.your_app_password

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        server.login(msg['From'], password)
        for destinationEmail in listOfEmail:
            if checkEmail(destinationEmail):
                try:
                    server.sendmail(msg['From'], destinationEmail, msg.as_string())
                    print("sending to {}".format(destinationEmail))
                    output['success'] += 1
                except Exception as e:
                    print("Error: {}".format(e))
                    output['failed'] += 1
            else:
                print("[INFO]: {} is not a valid email.".format(destinationEmail))
                output['invalid'] += 1

        return output
    
# from email_generator import PyEmailer

# your_email_id = "gayathrichandrasekar98@gmail.com"
# your_app_password = "mvgw mwav wzho rtme"
# email_subject = "Test Email"
# email_content = "<h4> ***Auto-generated email. Please ignore*** </h4>"
# listOfEmail = ["bharathkrishnaa5@gmai34l.com ", "vishruthimanick@gmail.com "]

# pyemail = PyEmailer(your_email_id, your_app_password)

# if __name__ == "__main__":
#     pyemail.sendEmail(email_subject, email_content, listOfEmail)

def send_periodic_emails():
    your_email_id = "gayathrichandrasekar98@gmail.com"
    your_app_password = "mvgw mwav wzho rtme"
    email_subject = "Test Email"
    email_content = "<h1> ***Auto-generated email. Please ignore***</h1>"
    email_list = ["bharathkrishnaa5@gmail.com ", "vishruthimanick@gmail.com "]

    pyemail = PyEmailer(your_email_id, your_app_password)
    result = pyemail.sendEmail(email_subject, email_content, email_list)
    print("Periodic email sending result:", result)

schedule.every(1).day.at("16:00").do(send_periodic_emails)

while True:
    schedule.run_pending()
    time.sleep(1)
