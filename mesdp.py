import yaml
import os
import requests
import logging
import json
import ast
from pprint import pprint

path = os.environ["WORKDIR"]

with open(path + "/trigger_plugins/mesdp/dnifconfig.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    mesdp_key = cfg['trigger_plugin']['MESDP_API_KEY']
    mesdp_server = cfg['trigger_plugin']['MESDP_SERVER']
    mesdp_port = cfg['trigger_plugin']['MESDP_PORT']
    mesdp_name = cfg['trigger_plugin']['MESDP_NAME']
def select_template(dt,tmp_name):
    try:
        with open(path+"/trigger_plugins/mesdp/"+tmp_name, "r") as f:
            ds = str(f.read())
        d = dict((x[1], '~~') for x in ds._formatter_parser())
        d.update(dt)
        c = ds.format(**d)
        c = c.replace("\n", "")
        json_content = ast.literal_eval("{" + c + "}")
        #print "printing c...",c
        #json_content["requestType"] = "Service Request"
        #json_content["requesttemplate"] = "Spyware Detect on PaloAlto"
        json_content = {"operation": {"details": json_content}}
        #pprint(json_content)
        url = "https://{0}:{1}/sdpapi/request?OPERATION_NAME=ADD_REQUEST&TECHNICIAN_KEY={2}".format(mesdp_server,
                                                                                                    mesdp_port,
                                                                                                    mesdp_key)
        args = {'OPERATION_NAME': 'ADD_REQUEST', 'TECHNICIAN_KEY': mesdp_key, 'format': 'json',
                'INPUT_DATA': json.dumps(json_content)}

        response = requests.post(url, params=args, verify=False)
        #print "printing response: ", response.content
        resp_data = response.json()
        #print "Status code: {}".format(response.status_code)
        #s = str(response.content)
        #root = ET.fromstring(s)
        out = {}
        out["$MESDPMessage"]=resp_data["operation"]["result"]["message"]
        out["$MESDPStatus"]=resp_data["operation"]["result"]["status"]
        
        out["$MESDPWorkOrderID"]=resp_data["operation"]["Details"]["WORKORDERID"]
        
        '''
        out['$MESDPStatus'] = root[0][0][0][1].text
        out['$MESDPMessage'] = root[0][0][0][2].text
        out['$MESDPWorkOrderID'] = root[0][0][1][0].text
        '''
        return out

    except Exception, e:
        out = {}
        s1 = "Error in API {}".format(e)
        logging.error("MESDPError :{}".format(e))
        out['$MESDPErrorMessage'] = s1
        #out["$MESDPStatus"]=response.status_code
        #out["$MESDPContent"]=response.content
        return out


def create_ticket(inward_array, var_array):
    tmp_lst = []
    var_array[0] = var_array[0].strip()
    var_array[1] =str(var_array[1]).replace(" ", "")
    for i in inward_array:
        try:
            if var_array[1] in i:
                tmp_dict = {}
                tmp_dict.update(i)
                tmp_dict['$Name'] = mesdp_name
                tmp_dict['$Subject'] = str(var_array[0].strip('"'))+str(i[var_array[1]])
                if (len(var_array) == 3):
                    fname = var_array[2].replace(" ", "")
                else:
                    fname ="default.txt"
                d = select_template(tmp_dict, fname)
                i.update(d)
                tmp_lst.append(i)
        except Exception, e:
            tmp_lst.append(i)
            logging.error("%s", e)
    return tmp_lst
