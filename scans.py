#!/usr/bin/python
import sys, getopt
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json

smart_check_url=''
smart_check_userid=''
smart_check_password=''
scan_registry=''
scan_repository=''
scan_tag='latest'
aws_region='ap-southeast-1'
aws_access_key=''
aws_secret=''
scan_name='Python Script Scan'
scan_id=''
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def init(argv): 
   
   try:
      opts, args = getopt.getopt(argv,"h:v",["smart_check_url=","smart_check_userid=","smart_check_password=","scan_registry=","scan_repository=","scan_tag=","aws_region=","aws_access_key=","aws_secret=","scan_id="])
   
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

      elif opt in ("--scan_registry"):
         global scan_registry
         scan_registry = arg

      elif opt in ("--scan_repository"):
         global scan_repository

         scan_repository = arg

      elif opt in ("--scan_tag"):
         global scan_tag
         scan_tag = arg
         
      elif opt in ("--aws_region"):
         global aws_region
         aws_region = arg

      elif opt in ("--aws_id"):
         global aws_id
         aws_id = arg

      elif opt in ("--aws_secret"):
         global aws_secret
         aws_secret = arg

      elif opt in ("--scan_name"):
         global scan_name
         scan_name = arg

      elif opt in ("--scan_id"):
         global scan_id
         scan_id = arg

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
    print(x['id'])


def generate_request(token):
    #print("----- Generating Request -----")
    payload = {}
    if scan_id:
        #print("scan ID Not Empty ")
        payload['id'] = scan_id
    
    
    payload['name'] = scan_name
    payload['source']={}
    payload['source']['credentials']={}
    payload['source']['credentials']['aws']={}
    payload['source']['type']="docker"
    payload['source']['registry']=scan_registry
    payload['source']['repository']=scan_repository
    payload['source']['tag']=scan_tag
    payload['source']['credentials']['aws']['region']=aws_region
    payload['source']['credentials']['aws']['accessKeyID']=aws_access_key
    payload['source']['credentials']['aws']['secretAccessKey']=aws_secret
    #print(payload)
    headers = {
            'authorization': "Bearer " + token,
            'content-type': "application/json",
        }
    r = requests.post('https://'+smart_check_url+'/api/scans', json=payload, headers=headers, verify=False)
    #print(r)
    x = json.loads(r.text)
    #print(x)
    #print(x['id'])
    return x['id']

init(sys.argv[1:])
#print(smart_check_userid)
token = get_token(smart_check_userid,smart_check_password)
#print (token['token'])
scan_id = generate_request(token['token'])
get_scan(token['token'],scan_id)