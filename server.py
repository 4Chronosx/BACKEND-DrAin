import json
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tools.swmm_extract import get_node_flooding_summary
from tools.swmm_tools import simulate_new

app = FastAPI()

# Allow local frontend + railway domain
origins = [
    "http://localhost:3000",
    "https://web-production-2976d.up.railway.app/",
    "https://pjdsc-drain.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    nodes: dict
    links: dict
    rainfall: dict

@app.post("/run-simulation")
def run_simulation(request: SimulationRequest):
    nodes = request.nodes
    links = request.links
    rainfall = request.rainfall
    try:
        simulate_new('data/Mandaue_Drainage_Network.inp', nodes, links, rainfall)
    except Exception as e:
        print(f"Unexpected error occured: {e}")

    jsonData = None
    data = {}
    try:
        if rainfall:
            jsonData = get_node_flooding_summary('data/Mandaue_Drainage_Network_mod.rpt','data/Mandaue_Drainage_Network_mod.out')
        else:
            jsonData = get_node_flooding_summary('data/Mandaue_Drainage_Network.rpt', 'data/Mandaue_Drainage_Network.out')
        data = json.loads(jsonData)
    except Exception as e:
        print(f"Unexpected error occured: {e}")
    finally:
        return data

