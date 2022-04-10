import requests
import time
import json


data = requests.get('https://ghoapi.azureedge.net/api/AIR_41').json()
with open('air.json','w') as f:
    json.dump(data,f,indent=4)
print(len(data['value']))