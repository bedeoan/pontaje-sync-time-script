import requests
import json
import os
import sys

### Autheticatie requests ###
f = open(".env", "r")
env = f.read()
api=env.split('\n')[0].split('=')[1]
email=env.split('\n')[1].split('=')[1]
password=env.split('\n')[2].split('=')[1]
localip=env.split('\n')[3].split('=')[1]

def setTokenInFile():
    myobj = {
        'device_name': 'synctime',
        'email': email,
        'device_name': password,
    }
    payload = "{\"email\":\""+email+"\",\"password\":\""+password+"\",\"remember\":true,\"device_name\":\"vanzari\"}"
    headers = {
    'authority': api,
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", api + '/api/sanctum/token', headers=headers, data=payload)
    if response.status_code == 200:
        f = open(".token", "a")
        f.write(response.text)
        f.close()
        return response.text
    # else: notify on slack serve unreachable !!!

def getHeadersAuth():
    try:
        f = open(".token", "r")
        token = f.read()
        print(token)
    except:
        token = setTokenInFile()

    headersAuth = {
        'Authorization': 'Bearer ' + token
    }
    resp =  requests.get(api + '/api/test-timesync', headers=headersAuth)

    if resp.status_code != 200:
        # if token from file has expired we relogin
        token = setTokenInFile()
        headersAuth = {
            'Authorization': 'Bearer ' + token
        }
    return headersAuth

# #token is valid we go and have fun
# headersAuth = getHeadersAuth()
# resp = requests.get(api + '/api/timelogs/46313', headers=headersAuth)
# print(resp)

## End of authentication ####

