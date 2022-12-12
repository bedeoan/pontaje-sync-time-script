import requests
import json
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK, const
import zk

#import login
import login
headersAuth = login.getHeadersAuth()
api=login.api
localip=login.localip
#--
conn = None
zk = ZK(localip, port=4370, verbose=True, force_udp='force')

conn = zk.connect()
try:
    conn.set_user()
    users = conn.get_users()
    usersById = {}
    apiusersById = {}
    for user in users:
        usersById[user.uid] = user

    response = requests.get(api + '/curentEmployees',headers=headersAuth)
    employeesfromApi = response.json() 
    print('try sync..')
    for emp in employeesfromApi:
        print(emp['id'])
        print(emp['name'])
        print(emp['auth_code'])
        apiusersById[emp['id']] = emp
        if emp['auth_code'] is not None:
            if emp['id'] in usersById.keys():
                try:
                    conn.set_user(uid=emp['id'], name=emp['name'], privilege=const.USER_DEFAULT, card=int(emp['auth_code']), user_id=emp['id'])
                except ValueError:
                    print('empty')
            else:
                try:
                    conn.set_user(uid=emp['id'], name=emp['name'], privilege=const.USER_DEFAULT, card=int(emp['auth_code']), user_id=emp['id'])
                except ValueError:
                    print('empty')
    for user in users:
        if user.uid not in apiusersById.keys():
            print(user.uid)
            print(user.name)
            conn.delete_user(user.uid)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()



