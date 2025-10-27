from pyswmm import Simulation, Nodes, Links, RainGages, SimulationPreConfig
import math


def modify_nodes(nodes_ls, sim):
    nodes = Nodes(sim)
    for node in nodes_ls:
        node_obj = nodes_ls[node]
        nodes[node].invert_elevation = node_obj['inv_elev']
        nodes[node].initial_depth = node_obj['init_depth']
        nodes[node].ponding_area = node_obj['ponding_area']
        nodes[node].surcharge_depth = node_obj['surcharge_depth']

def modify_links(links_ls, sim):
    links = Links(sim)
    for conduit in links_ls:
        for link in links:
          link_obj = links_ls[conduit]
          if link.linkid.endswith(conduit):
            links[link.linkid].flow_limit = link_obj['init_flow']
            links[link.linkid].upstrm_offset_depth = link_obj['upstrm_offset_depth']
            links[link.linkid].downstrm_offset_depth = link_obj['downstrm_offset_depth']
            links[link.linkid].avg_conduit_loss = link_obj['avg_conduit_loss']
            links = Links(sim)

def modify_raingage(raingage_ls, sim):
    raingages = RainGages(sim)
    for raingage in raingage_ls:
        print(raingages[raingage].total_precip)

def generate_rainfall_event(total_rain_mm, duration_hr, interval_min=5, pattern="triangular"):
    import numpy as np

    times = np.arange(0, duration_hr + interval_min/60, interval_min/60)
    n = len(times)

    if pattern == "uniform":
        shape = np.ones(n)
    elif pattern == "triangular":
        shape = np.concatenate([
            np.linspace(0, 1, n//2),
            np.linspace(1, 0, n - n//2)
        ])
    elif pattern == "chicago":
        peak_pos = int(n * 0.4)
        up = np.linspace(0, 1, peak_pos)
        down = np.linspace(1, 0, n - peak_pos)
        shape = np.concatenate([up, down])
    else:
        raise ValueError("Pattern must be 'uniform', 'triangular', or 'chicago'.")

    shape = shape / shape.sum() * total_rain_mm
    intensities = shape * (60 / interval_min)

    rainfall_series = [(round(t, 2), round(i, 2)) for t, i in zip(times, intensities)]
    return rainfall_series

def simulate_new(inp_path, nodes_ls, links_ls, rainfall_obj, dt_sec=300):
    if not inp_path:
        raise ValueError("Input file path is empty.")

    sim_conf = None

    # Generate rainfall event
    if rainfall_obj:
        # Create PreConfig
        sim_conf = SimulationPreConfig()

    

        timeseries_name = "TS_Rain"
        duration_hr = rainfall_obj.get('duration_hr', 1)
        total_mm = rainfall_obj.get('total_precip', 100)
        rainfall_series = generate_rainfall_event(total_mm, duration_hr)
        print("Rainfall series:", rainfall_series)

        if duration_hr < 24:
          if (duration_hr > math.floor(duration_hr)):
            hour = math.floor(duration_hr)
            mins = int((duration_hr - math.floor(duration_hr)) * 60)
            sim_conf.add_update_by_token("OPTIONS", "END_TIME", 1, f"{hour if hour >= 10 else '0' + str(hour)}:{mins if mins >= 10 else '0' + str(mins)}:00")
            sim_conf.add_update_by_token("OPTIONS", "END_DATE", 1, "01/01/2024")
          else:
            sim_conf.add_update_by_token("OPTIONS", "END_TIME", 1, f"{duration_hr if duration_hr >= 10 else '0' + str(duration_hr)}:00:00")
            sim_conf.add_update_by_token("OPTIONS", "END_DATE", 1, "01/01/2024")

        for row_num, (t, i) in enumerate(rainfall_series):
            hours = int(t)
            minutes = int(round((t - hours) * 60))
            sim_conf.add_update_by_token("TIMESERIES", timeseries_name, 1, f"{hours:02}:{minutes:02}", row_num)
            sim_conf.add_update_by_token("TIMESERIES", timeseries_name, 2, f"{i:.2f}", row_num)

        total_orig_series = 289 # (original steps for 24hr)
        expected_series = len(rainfall_series)
        print(f"orig: {total_orig_series} exp: {expected_series}")
        if total_orig_series > expected_series:
            for extra_idx in range(expected_series, total_orig_series):
                sim_conf.add_update_by_token("TIMESERIES", timeseries_name, 0, '', extra_idx)
                sim_conf.add_update_by_token("TIMESERIES", timeseries_name, 1, '', extra_idx)
                sim_conf.add_update_by_token("TIMESERIES", timeseries_name, 2, '', extra_idx)
            print(f"🧹 Removed {total_orig_series - expected_series} leftover timeseries entries")
        else:
            print("✅ Timeseries section matches expected length")

    # Run simulation with preconfig
    with Simulation(inp_path, sim_preconfig=sim_conf) as sim:
        if nodes_ls:
          modify_nodes(nodes_ls, sim)
        if links_ls:
          modify_links(links_ls, sim)

        for step in sim:
            pass
