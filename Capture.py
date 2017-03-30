#!/usr/bin/env python
#arg1:clusername, arg2:ambariUsername, arg3:ambariPassword. arg4:caseId
import sys
import requests
import json

getUrl = 'https://' + sys.argv[1] + '.azurehdinsight.net/api/v1/clusters/' + sys.argv[1] + '/hosts'
headers = {'X-Requested-By': '\"ambari\"', 'Cache-Control': 'no-cache'}
postUrl = 'https://' + sys.argv[1] + '.azurehdinsight.net/api/v1/clusters/' + sys.argv[1] + '/requests'
jdkUrl = 'https://' + sys.argv[1] + '.azurehdinsight.net/api/v1/resources'
auth = (sys.argv[2],sys.argv[3])
getRequest = requests.get(getUrl, auth=auth)

if(getRequest.ok):
    print 'Host list retrived, submitting Script Action now.'
    rawList= json.loads(getRequest.content)['items']
    hostList = []
    for token in rawList:
        hostList.append(str(token['Hosts']['host_name']))
    list = ''
    for token in hostList[:-1]:
        list = list + token + ','
    list = list + hostList[-1]
    data = { "RequestInfo": { "action": "run_customscriptaction", "context": "run_customscriptaction", "parameters": {"script_location":"https://smartsenseprod.blob.core.windows.net/scriptaction/Capture.sh", "script_params":sys.argv[4], "jdk_location":jdkUrl, "storage_account":"", "storage_key":"", "storage_container":"", "blob_name":"" } }, "Requests/resource_filters":[{"hosts":list}] }
    postRequest = requests.post(postUrl, data = json.dumps(data), headers=headers, auth=auth)
    if(postRequest.ok):
        print 'Script Action submitted successfully. Please see Ambari UI for: Background Operations Running'
    else:
        print 'Script Action failed with status code: ' + str(postRequest.status_code)
else:
    print 'Failed to retrive host list, with the following arguments:'
    print 'arg1: Cluster name: ' + sys.argv[1]
    print 'arg2: Ambari username: ' + sys.argv[2]
    print 'arg3: Ambari password: ' + sys.argv[3]
    print 'arg3: case ID: ' + sys.argv[4]






