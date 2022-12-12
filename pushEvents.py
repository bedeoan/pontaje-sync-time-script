# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import datetime
CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)
 
from zk import ZK, const
 #import login
import login
headersAuth = login.getHeadersAuth()
api=login.api
localip=login.localip
#--

conn = None
zk = ZK(localip, port=4370, verbose=True,force_udp='force')
 
def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60
try:
    response = requests.get(api + '/api/option/sync',headers=headersAuth)
    lastSync = response.content
    print('last sync')
    print(lastSync)
    conn = zk.connect()
    conn.disable_device()
    users = conn.get_users()
    usersById = {}
 
    attendences = conn.get_attendance()
    from datetime import datetime as dt
    lastsync = dt.strptime(str(lastSync, 'utf-8'), "%Y-%m-%d")
    attforsync = []
    today = dt.today().strftime('%Y-%m-%d')
   
    # attforsync contine toate evenimentele care nu au fost sincuite
    for att in attendences:
        if att.timestamp >= lastsync:
            attforsync.append(att)
   
    # iterez peste fiecare event- iau useru caut start,end form\ez pache si push
    print(len(attforsync))
    for att in attforsync:
        dayInSync = att.timestamp.strftime('%Y-%m-%d')
        start = dt.strptime('2060-01-01', '%Y-%m-%d')
        end = dt.strptime('2010-01-01', '%Y-%m-%d')
        uid = att.user_id
 
        if usersById.get(att.user_id) == None:
            for attS in attforsync:
                if attS.timestamp.strftime('%Y-%m-%d') == dayInSync and attS.timestamp < start and attS.user_id == uid:
                    start = attS.timestamp
                if attS.timestamp.strftime('%Y-%m-%d') == dayInSync and attS.timestamp > end and attS.user_id == uid:
                    end = attS.timestamp
   
            hours = end - start
            h = days_hours_minutes(hours)[1]
            resp =  requests.get(api + '/api/getEmployeeTime/' + att.user_id + "/date/" + start.strftime('%Y-%m-%d'),headers=headersAuth);
            try:
                entity = resp.json()
                #daaca nu a iesit omul nu dac nici un update sau daca nu exisa modificari la utima iesire
                if entity['end'] == end.strftime('%Y-%m-%d %H:%M:%S') or end == dt.strptime('2010-01-01', '%Y-%m-%d'):
                    print ('nu trebuie update')
                else:
                    print('Update existing event ' + str(entity['id']) + ' for user ' + att.user_id)
                    payload = {
                        'hours' : h,
                        'end' : end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    print('pathing existing end')
                    resp =  requests.patch(api + '/api/timelogs/' + str(entity['id']),headers=headersAuth, data= payload)
            except ValueError:
                print('new Event for user ' + att.user_id)
                if start != dt.strptime('2060-01-01', '%Y-%m-%d'):
                    payload = {
                        'employee_id': att.user_id,
                        'hours' : h,
                        'date' : start.strftime('%Y-%m-%d'),
                        'start' : start.strftime('%Y-%m-%d %H:%M:%S'),
                        'end' : end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    print('new value post')
                    print(payload)
                    requests.post(api + '/api/timelogs',headers=headersAuth, data= payload)
    requests.post(api + '/api/option/sync/value/' + today,headers=headersAuth)
    print('update time today sinc')
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.enable_device()
        conn.disconnect()
