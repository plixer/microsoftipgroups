import json
import requests
from scrut_api import ReportAPI, Requester


#gather data from microsoft, and convert it to JSON. 
ip_data_raw = requests.get("https://endpoints.office.com/endpoints/Worldwide?ClientRequestId=b10c5ed1-bad1-445f-b386-b919946339a7")
microsoft_ips = ip_data_raw.json()

print('Microsoft Data Retrieved')

report_params = ReportAPI()
scrutinizer_requester = Requester(
    authToken="your-auth-token-here",
    hostname="your-scrutinizer-hostname-here"
)


#simple way of remove all duplicate IP Adddresses from the multiple lists. 
def remove_duplicates(list_of_items):
    print('Removing Duplicate IP addresses')
    for group in list_of_items:
        list_of_items[group] = set(list_of_items[group])
    return list_of_items

#function to filter microsoft data for groups we want, and return data we want. 
def filter_microsoft_data(microsoft_ips):

    groups_to_add = {
        'Exchange':[],
        'Skype':[],
        'SharePoint':[]
    }
    print('Filtering Data to Add Desired Groups')
    for service in microsoft_ips:
        try:
            #since we are creating IP groups, we only want the data that contains ips.
            if service['serviceArea'] in groups_to_add and service['ips']:
                groups_to_add[service['serviceArea']].extend(service['ips'])
        except:
            pass


    groups_to_add = remove_duplicates(groups_to_add)      
    return groups_to_add

#function to use the API to create the group data.
def use_api_to_create_groups(microsoft_ips, report_params, scrutinizer_requester):
    
    for ip_group in microsoft_ips:
        data_for_api = []
        for ip_subnet in microsoft_ips[ip_group]:
            subnet = ip_subnet.split('/')[0]
            mask = ip_subnet.split('/')[1]
            data_for_api.append({"type":"network", "address":subnet, "mask":mask})
        
        #Do a quick check to convert Skype to include teams as well.
        try:
            if ip_group =='Skype':
                ip_group = 'Skype or Teams'
        except:
            pass

        report_params.create_group(ip_group, json.dumps(data_for_api))
        scrutinizer_requester.make_request(report_params)




microsoft_ips = filter_microsoft_data(microsoft_ips)

use_api_to_create_groups(microsoft_ips, report_params, scrutinizer_requester)






