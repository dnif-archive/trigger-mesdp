# Manage Engine Service Desk Plus (mesdp) 
  https://www.manageengine.com/products/service-desk/
### Overview
ServiceDesk Plus is a game changer in turning IT teams from daily fire-fighting to delivering awesome customer service. It provides great visibility and central control in dealing with IT issues to ensure that businesses suffer no downtime. This all-in-one solution delivers comprehensive Incident Management, Self-service portal, Knowledge base, Multi-site support, SLA Management and Help Desk Reports. 

 
##### PRE-REQUISITES to use mesdp and DNIF  
Outbound access required for github to clone the plugin

| Protocol   | Source IP  | Source Port  | Direction	 | Destination Domain | Destination Port  |  
|:------------- |:-------------|:-------------|:-------------|:-------------|:-------------|  
| TCP | DS,CR,A10 | Any | Egress	| github.com | 443 |

 
## mesdp trigger plugin functions
Details of the function that can be used with the mesdp trigger is given in this section.

### create_ticket 
This function allows for creating a ticket against an observerd event using the defined (custom/default template)  .

### Input  
- Subject of ticket.(Note Commas(,) cannot be used as they are used for Input parameters seperation ) 
- Event Field prenset in the event .
- Template name to be triggered.(Note if this field is not provided the default template gets triggered)   

### Example
```
_fetch * from event where $Action=LOGIN_FAIL limit 1
>>_trigger api mesdp create_ticket Login Failed for User : ,$User , default.xml
```

### Output  
![mesdp](https://user-images.githubusercontent.com/37173181/44776438-b7631180-ab95-11e8-8f47-a42ea723f424.jpg)


The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $MESDPMessage     | Message for the API ticket request |
| $MESDPStatus      | can be Success/Fail in creating the ticket|
| $MESDPWorkOrderID | Work order id associated with the newly created ticket |


### Using the mesdp API and DNIF  
The mesdp API is found on github at 

  https://github.com/dnif/trigger-mesdp

The following process has to be repeated on all of the following components

### Getting started with mesdp API and DNIF

1. ####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. ####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/trigger_plugins/
```
3. ####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-mesdp.git mesdp
```
4. ####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/mesdp/’` folder path and open dnifconfig.yml configuration file     
    
   Replace the tags: <Add_your_*> with your mesdp credentials
```
trigger_plugin:
  MESDP_API_KEY: <Add_your_technical_key_here>
  MESDP_SERVER: <Add_your_server/host_details_here>
  MESDP_PORT: <Add_your_mesdp_port_here>
  MESDP_NAME: <Add_your_requester_name_here>

```
5. #### For using userdefined templates 
   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/mesdp/’` folder path and paste your template.xml file here.
   #### Note:  
       Refer to default.xml template to create your customised templates
  
