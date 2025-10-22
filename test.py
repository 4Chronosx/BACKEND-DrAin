import json
import requests

myNodes = {

    'I-4': {'inv_elev': 16, 'init_depth': 0, 'ponding_area': 0, 'surcharge_depth': 0},
}

myLinks = {
   
}

rainfall = {
    'total_precip': 104.9,
    'duration_hr': 1,
}

data = {
    'nodes': myNodes,
    'links': myLinks,
    'rainfall': rainfall
}

url = 'https://web-production-2976d.up.railway.app/run-simulation'

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response: ", response.json())
