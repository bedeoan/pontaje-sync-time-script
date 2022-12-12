import requests
import json
import os
import sys

import login
headersAuth = login.getHeadersAuth()
api=login.api

resp = requests.get(api + '/api/timelogs/46313', headers=headersAuth)