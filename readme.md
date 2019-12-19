## Create IP Groups for SharePoint, Exchange, Teams and Skype based of Microsofts published list of IPs. 



### Update AuthToken and Scrutinizer Hostname

Prior to running this script users will need to update the hostname and api key found in the *scrutinizer_requester* variable in the microsoftips.py file. 

```
scrutinizer_requester = Requester(
    authToken="your-auth-token-here",
    hostname="your-scrutinizer-hostname-here"
)
```

Save the file after updating it. 

### Running the Script
Install the required packages, the script uses the requests library to comminicate with Scrutinizer's API as well as Microsoft. 

    pip install -r requirements.txt 


Run the script 

    python microsoftips.py 


