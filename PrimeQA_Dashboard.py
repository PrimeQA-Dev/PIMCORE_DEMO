import logging
import os
import requests
import json
import TestCase
from dotenv.main import load_dotenv
load_dotenv()


AWS_IP = os.environ['AWS_IP']
Project_API_Key = os.environ['Project_API_Key']
global Login_Token


def Eleven_Automation_Login():
    logging.info("Entered into Eleven_Automation_Login method....")
    url = AWS_IP + "api/v1/auth/login"
    # url = AWS_IP + "login"

    payload = json.dumps({
        "email": os.environ['Email_Id'],
        "password": os.environ['PSWD']
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Og=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if str(response.status_code) == "200":
        resp_data = response.json()
        logging.info(resp_data.get("token"))
        Login_Token = resp_data.get("token")
    else:
        Login_Token = None

    logging.info("Exiting from  Eleven_Automation_Login method....")
    return Login_Token

def Eleven_Automation_Iteration(Iteration_data, RT_Login_Token):
    logging.info("Entered into Eleven_Automation_Iteration method....")
    url = AWS_IP + "api/v1/iterations/" + Project_API_Key
    # url = AWS_IP + "iterations/" + Project_API_Key
    # payload = json.dumps(dict(Iteration_data),default=str)
    logging.info(url)

    payload = json.dumps({
        "iterationId": dict(Iteration_data).get("Project Name"),
        "testType": dict(Iteration_data).get("Test Type"),
        "browserUsed": dict(Iteration_data).get("Browser Used"),
        "browserVersion": dict(Iteration_data).get("Browser Version"),
        "executionStartTime": dict(Iteration_data).get("Test Execution Start Time"),
        "executionEndTime": dict(Iteration_data).get("Test Execution End Time")
    },default=str)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+str(RT_Login_Token)
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logging.info(response.status_code)
    logging.info(response.text)

    if str(response.status_code) == "201" or str(response.status_code) == "200":
        resp_data = response.json()
        logging.info(resp_data['iteration']['_id'])
        Iteration_Id = resp_data['iteration']['_id']
    else:
        Iteration_Id = None

    logging.info("Exiting from Eleven_Automation_Iteration method....")
    return Iteration_Id

def Eleven_Automation_TestCase(RT_Login_Token, RT_Iteration_Id):
    url = AWS_IP+"api/v1/testcases/"+RT_Iteration_Id
    # url = AWS_IP + "testcases/" + RT_Iteration_Id

    logging.debug(TestCase.Success_List)
    testcase_list = []
    i = 0
    while i < len(TestCase.Success_List):
        element = {
            "testCaseId": TestCase.Success_List[i][0],
            "testCaseSummary": TestCase.Success_List[i][1],
            "result": TestCase.Success_List[i][2],
            "executionTime": TestCase.Success_List[i][4],
            "comments": TestCase.Success_List[i][3],

        }
        i += 1
        testcase_list.append(element)
    payload = json.dumps(testcase_list)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+RT_Login_Token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logging.info(response.status_code)

def Dashboard_main(Iteration_data):
    logging.info("Entered into Dashboard_main method....")
    RT_Login_Token = Eleven_Automation_Login()
    RT_Iteration_Id = Eleven_Automation_Iteration(Iteration_data, RT_Login_Token)
    # RT_Login_Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NDcwZWJmNjA4YjczNWQ5YjVmNGExNzgiLCJpYXQiOjE2ODU0NDkwNjEsImV4cCI6MTY4NTUzNTQ2MX0.5jVm_-qd0KlkTpL3gQU_EV5DnQiiUhzLRDO7piQiLQE"
    # RT_Iteration_Id= "6475e9655840a38d9f3e2229"
    Eleven_Automation_TestCase(RT_Login_Token, RT_Iteration_Id)
    logging.info("Exiting from Dashboard_main method....")
