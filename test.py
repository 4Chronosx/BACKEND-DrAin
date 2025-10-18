import json
from tools.swmm_tools import simulate_new
from tools.swmm_extract import get_node_flooding_summary

myNodes = {
    'I-0': {'inv_elev': 0, 'init_depth': 0, 'ponding_area': 0, 'surcharge_depth': 0},
    'I-1': {'inv_elev': 16, 'init_depth': 2, 'ponding_area': 1, 'surcharge_depth': 0},
    'I-2': {'inv_elev': 30, 'init_depth': 0, 'ponding_area': 0, 'surcharge_depth': 0},
    'I-4': {'inv_elev': 30, 'init_depth': 0, 'ponding_area': 0, 'surcharge_depth': 2},
}

myLinks = {
    'C-37': {'init_flow': 0.5, 'upstrm_offset_depth': 5, 'downstrm_offset_depth': 5, 'avg_conduit_loss': 0},
    'C-2': {'init_flow': 0, 'upstrm_offset_depth': 10, 'downstrm_offset_depth': 2, 'avg_conduit_loss': 0.5},
    'C-112': {'init_flow': 1.5, 'upstrm_offset_depth': 0, 'downstrm_offset_depth': 0, 'avg_conduit_loss': 100},
}

rainfall = {
    #'total_precip': 140,
    #'duration_hr': 0.5,
}

simulate_new('data/Mandaue_Drainage_Network.inp', myNodes, myLinks, rainfall)

jsonData = None

if rainfall:
    jsonData = get_node_flooding_summary('data/Mandaue_Drainage_Network_mod.rpt','data/Mandaue_Drainage_Network_mod.out')
else:
    jsonData = get_node_flooding_summary('data/Mandaue_Drainage_Network.rpt', 'data/Mandaue_Drainage_Network.out')
data = json.loads(jsonData)

print(data['nodes_dict']['I-4']['Hours_Flooded'])