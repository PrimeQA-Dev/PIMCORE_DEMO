import sys
import logging
import datetime
import os
from email import encoders
from email.mime.base import MIMEBase
from pretty_html_table import build_table
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import pandas as pd
import TestCase
import PrimeQA_Dashboard
from zoneinfo import ZoneInfo
from dotenv.main import load_dotenv

load_dotenv()
AWS_IP = os.environ['AWS_IP']
# print(sys.argv[1])

Today_date = datetime.date.today()
# region

# logging.basicConfig(format="[%(asctime)s.%(msecs)03d][%(levelname)s]:[%(lineno)s] - %(message)s", level=logging.INFO,
#                     datefmt='%Y-%m-%d %H:%M:%S')

LOGGER_FILENAME = os.path.join(os.getcwd(), str(Today_date) + "-Demo.txt")
logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d][%(levelname)s]:[%(lineno)s] - %(message)s",
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(LOGGER_FILENAME, 'a'),
        logging.StreamHandler()
    ])

SENDER_MAIL = 'TestMailPrimeQA@gmail.com'
SENDER_PWD = 'pzvjbtwvwcodzphu'
Tester = 'sachin@primeqasolutions.com'
cc = os.getenv("Email")
# cc = "sachin@primeqasolutions.com"
Recipents = cc.split(",") + [Tester]


# cc = 'sachin@primeqasolutions.com,sachin@primeqasolutions.com'
# Recipents = cc.split(",") + [Tester]


# endregion

def Send_Mail():
    logging.info("Sending Mail...........")
    message = MIMEMultipart()
    message['Subject'] = 'Demo- Automation Results'
    message['From'] = SENDER_MAIL
    message['To'] = Tester
    message['Cc'] = cc
    message.attach(MIMEText('Hi', 'plain', 'utf-8'))
    message.attach(MIMEText('\n', 'plain', 'utf-8'))
    # email_body ="""<p>
    # Please find below Test Report for Automation Testing.
    # Go to the page: <a href="http://43.204.236.58/">click here</a>
    # </p>"""
    email_body = """\
    	<html>
    	  <head></head>
    	  <body>
    	    <p> 
                Please find below Test Report for Automation Testing.
                Go to the page: <a href=""" + AWS_IP + """>click here</a>
            </p>
    	  </body>
    	</html>
    	"""

    message.attach(MIMEText(email_body, 'html'))
    message.attach(MIMEText('Please login with your credentials:', 'plain', 'utf-8'))
    # message.attach(MIMEText('\nUsername- sachin.patel@primeqa.com', 'plain', 'utf-8'))
    # message.attach(MIMEText('\npassword- Patel@1234', 'plain', 'utf-8'))
    message.attach(MIMEText('\nProject key - 6470ec7f08b735d9b5f4a17d', 'plain', 'utf-8'))
    message.attach(MIMEText('\n', 'plain', 'utf-8'))
    #
    filename = LOGGER_FILENAME
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= Logs")
    message.attach(part)

    message.attach(MIMEText('\n\n', 'plain', 'utf-8'))
    message.attach(MIMEText('  THIS IS SYSTEM GENERATED MAIL.', 'plain', 'utf-8'))
    msg_body = message.as_string()
    try:
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], SENDER_PWD)
        server.sendmail(message['From'], Recipents, msg_body)
        server.quit()
        logging.info("Mail Sent successfully")
    except Exception as e_mail:
        logging.error("Mail sending Failed")
        logging.error(e_mail)


def TestReport_Generation():
    global Test_Report_Table
    global Test_Report_DF
    global dash_report
    driver = webdriver.Chrome()
    logging.info("Entered into TestReport_Generation()")
    Test_Report = [["Project Name", "Eclipton"], ["Test Type", "Automation"], ["Browser Used", "Chrome"],
                   ["Browser Version", driver.capabilities['browserVersion']],
                   ["Test Execution Start Time", Execution_StartTime],
                   ["Test Execution End Time", Execution_EndTime], ["Test Pass", TestCase.SuccessCount],
                   ["Test Fail", TestCase.FailureCount],
                   ["Total Test Cases", int(TestCase.SuccessCount + TestCase.FailureCount)]]
    Test_Report_DF = pd.DataFrame(Test_Report, columns=("Summary", "Details"))
    Test_Report_Table = build_table(Test_Report_DF, "blue_dark", text_align='justify')
    driver.quit()
    dash_report = [["Project Name",
                    "Batch-" + str((datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata'))).strftime('%Y-%m-%d_%H-%M-%S'))],
                   ["Test Type", "Automation"], ["Browser Used", "Chrome"],
                   ["Browser Version", driver.capabilities['browserVersion']],
                   ["Test Execution Start Time", Execution_StartTime],
                   ["Test Execution End Time", Execution_EndTime]]
    logging.info("Exiting from TestReport_Generation()")


def Appending_list(L1, L2):
    L1 = [[*i, j] for i, j in zip(L1, L2)]
    TestCase.Success_List = L1
    return L1


def main():
    global Execution_StartTime
    global Execution_EndTime
    Execution_StartTime = datetime.datetime.now()

    TestCase.test_demo_1()
    # TestCase.test_demo_2()
    TestCase.test_demo_3()

    Execution_EndTime = datetime.datetime.now()
    Appending_list(TestCase.Success_List, TestCase.Execution_time)
    TestReport_Generation()
    PrimeQA_Dashboard.Dashboard_main(dash_report)
    Send_Mail()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(1)
