import json
import requests

from tools.swmm_extract import get_node_flooding_summary_with_vulnerability
from tools.swmm_tools import simulate_new

myNodes = {

    'I-4': {'inv_elev': 16.10, 'init_depth': 0, 'ponding_area': 0, 'surcharge_depth': 0},
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

#url = 'https://web-production-2976d.up.railway.app/run-simulation'

#response = requests.post(url, json=data)

#print("Status:", response.status_code)
#print("Response: ", response.json())


simulate_new('data/Mandaue_Drainage_Network.inp', myNodes, myLinks, rainfall)

if rainfall:
    jsonData = get_node_flooding_summary_with_vulnerability('data/Mandaue_Drainage_Network_mod.rpt','data/Mandaue_Drainage_Network_mod.out')
else:
    jsonData = get_node_flooding_summary_with_vulnerability('data/Mandaue_Drainage_Network.rpt', 'data/Mandaue_Drainage_Network.out')
data = json.loads(jsonData)
print(data['nodes_dict']['I-4'])

