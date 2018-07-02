#!/usr/bin/python
import sys, getopt
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json

smart_check_url=''
smart_check_userid=''
smart_check_password=''
scan_id=''
output='status'
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def init(argv): 
   
   try:
      opts, args = getopt.getopt(argv,"h:v",["smart_check_url=","smart_check_userid=","smart_check_password=","scan_id=","output="])
   
   except getopt.GetoptError as error:
      print 'Error Not enough Arguments'
      print str(error)
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print 'scans.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("--smart_check_url"):
         global smart_check_url
         smart_check_url = arg

      elif opt in ("--smart_check_userid"):
        global smart_check_userid
        smart_check_userid = arg
         
      elif opt in ("--smart_check_password"):
        global smart_check_password
        smart_check_password = arg

      elif opt in ("--scan_id"):
         global scan_id
         scan_id = arg

      elif opt in ("--output"):
         global output
         output = arg

def get_token(userid,password):
    #print("----- Generating Token ----- "+userid)
    payload = {'user':{'userID': userid, 'password': password}}
    r = requests.post('https://'+smart_check_url+'/api/sessions', json=payload, verify=False)
    #print(r)
    z = json.loads(r.text)
    #print(z['token'])
    return z


def get_scan(token,id):
    #print("----- Get Scan Data for "+id+" -----")
    headers = {
            'authorization': "Bearer " + token,
            'content-type': "application/json",
        }
    r = requests.get('https://'+smart_check_url+'/api/scans/'+id, headers=headers, verify=False)
    x = json.loads(r.text)
    if output == "status":
        print(x['status'])
    else:
        print(r.text)
    
    #print(x)

init(sys.argv[1:])
#print(smart_check_userid)
token = get_token(smart_check_userid,smart_check_password)
#print (token['token'])
get_scan(token['token'],scan_id)