import pandas as pd
from pyswmm import Output, NodeSeries
import json
import pickle
import numpy as np

def get_node_flooding_summary_with_vulnerability(rpt_file_path, out_file_path, model_path):
    """
    Convert Node Flooding Summary from RPT file to JSON format with hybrid structure.
    Includes all nodes from OUT file, with 0 values for non-flooded nodes.
    Adds vulnerability category and score predictions using the trained model.

    Args:
        rpt_file_path: Path to the input .rpt file
        out_file_path: Path to the input .out file
        model_path: Path to the vulnerability model pickle file (default: 'vulnerability_model_k4.pkl')

    Returns:
        str: JSON string containing all nodes with flooding summary data, vulnerability predictions in hybrid structure
    """

    # Read the RPT file
    with open(rpt_file_path, 'r') as file:
        content = file.read()

    # Load the vulnerability model
    print(f"\nLoading vulnerability model from {model_path}...")
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        kmeans = model['kmeans']
        scaler = model['scaler']
        cluster_ranking = model['cluster_ranking']
        categories = model['categories']
        scores = model['scores']

        print(f"✓ Model loaded with k={model['optimal_k']} clusters")
        print(f"Categories: {categories}")
    except Exception as e:
        print(f"⚠ Warning: Could not load vulnerability model: {e}")
        print("Proceeding without vulnerability predictions...")
        kmeans = None

    lines = content.split('\n')

    # Find the Node Flooding Summary section
    start_idx = None
    header_idx = None
    dash_count = 0

    for i, line in enumerate(lines):
        if 'Node Flooding Summary' in line:
            start_idx = i
            print(f"Found 'Node Flooding Summary' at line {i}")

        if start_idx is not None and '----------' in line:
            dash_count += 1
            if dash_count == 2:  # Second dash line marks start of data
                header_idx = i + 1
                print(f"Data should start at line {header_idx}")
                break

    # Extract data rows from RPT (only flooded nodes)
    flooded_nodes_data = {}

    if start_idx is not None and header_idx is not None:
        for i in range(header_idx, len(lines)):
            line = lines[i].strip()

            # Stop if we hit empty lines, another section, or dashes
            if not line:
                continue
            if line.startswith('*') or (line.startswith('-') and len(line) > 10):
                break

            # Parse the line - split by whitespace
            parts = line.split()

            # Debug: show what we're parsing
            if len(parts) < 6:
                print(f"Skipping line with {len(parts)} parts: {parts}")
                continue

            # Extract data - strip whitespace from node ID
            node = parts[0].strip()
            hours_flooded = float(parts[1])
            max_rate = float(parts[2])
            time_day = int(parts[3])
            # Convert "00:55" to decimal hours
            h, m = map(int, parts[4].split(':'))
            time_hour = m
            flood_volume = float(parts[5])

            flooded_nodes_data[node] = {
                'Hours Flooded': hours_flooded,
                'Maximum Rate (CMS)': max_rate,
                'Time of Max (days)': time_day,
                'Time of Max (hr:min)': time_hour,
                'Total Flood Volume (10^6 ltr)': flood_volume,
            }

        print(f"Successfully extracted {len(flooded_nodes_data)} flooded nodes from RPT")
    else:
        print("Node Flooding Summary section not found or incomplete in RPT file")

    # Get overflow timing from OUT file and build complete node list
    print(f"\nProcessing all nodes from {out_file_path}...")
    all_nodes_array = []
    all_nodes_dict = {}

    try:
        with Output(out_file_path) as out:
            node_series = NodeSeries(out)
            out_node_list = list(out.nodes)

            print(f"OUT file has {len(out_node_list)} total nodes")

            for node_id in out_node_list:
                node_data = node_series[node_id]
                flooding_ts = node_data.flooding_losses  # m3/s overflow indicator

                # Convert to DataFrame
                flood_df = pd.DataFrame(list(flooding_ts.items()), columns=["time", "flooding_m3s"])

                # Calculate time after raining
                if flood_df.empty:
                    minutes_after_rain = 0
                else:
                    # Use first timestamp as t=0
                    sim_start = flood_df["time"].iloc[0]

                    # Find first overflow time
                    first_overflow = flood_df[flood_df["flooding_m3s"] > 0]
                    if not first_overflow.empty:
                        overflow_time = first_overflow.iloc[0]["time"]
                        minutes_after_rain = round((overflow_time - sim_start).total_seconds() / 60, 2)
                    else:
                        minutes_after_rain = 0  # no overflow

                # Check if node is in the flooded nodes from RPT
                if node_id in flooded_nodes_data:
                    # Node has flooding data - convert to float for JSON serialization
                    hours_flooded = float(flooded_nodes_data[node_id]['Hours Flooded'])
                    max_rate = float(flooded_nodes_data[node_id]['Maximum Rate (CMS)'])
                    time_of_max_days = float(flooded_nodes_data[node_id]['Time of Max (days)'])
                    time_of_max_hr_min = flooded_nodes_data[node_id]['Time of Max (hr:min)']
                    total_flood_volume = float(flooded_nodes_data[node_id]['Total Flood Volume (10^6 ltr)'])
                    time_after_rain = float(minutes_after_rain)
                else:
                    # Node did not flood - all values are 0
                    hours_flooded = 0.0
                    max_rate = 0.0
                    time_of_max_days = 0.0
                    time_of_max_hr_min = 0
                    total_flood_volume = 0.0
                    time_after_rain = 0.0

                # Predict vulnerability if model is loaded
                vulnerability_category = "N/A"
                vulnerability_score = 0.0

                if kmeans is not None:
                    try:
                        # Create feature vector: [Hours_Flooded, Maximum_Rate_CMS, Time_of_Max_days, Time_After_Raining_min, Total_Flood_Volume]
                        # Note: Adjust feature order based on your model training
                        features = np.array([[hours_flooded, max_rate, time_of_max_days, time_after_rain, total_flood_volume]])
                        features_scaled = scaler.transform(features)
                        cluster = kmeans.predict(features_scaled)[0]
                        rank = cluster_ranking[cluster]
                        vulnerability_category = categories[rank]
                        vulnerability_score = float(scores[cluster])
                    except Exception as e:
                        print(f"Warning: Could not predict vulnerability for node {node_id}: {e}")

                # For ARRAY (includes Node ID)
                node_row_array = {
                    'Node': node_id,
                    'Hours_Flooded': hours_flooded,
                    'Maximum_Rate_CMS': max_rate,
                    'Time_of_Max_days': time_of_max_days,
                    'Time_of_Max_hr_min': time_of_max_hr_min,
                    'Total_Flood_Volume_10e6_ltr': total_flood_volume,
                    'Time_After_Raining_min': time_after_rain,
                    'Vulnerability_Category': vulnerability_category,
                    'Vulnerability_Score': vulnerability_score
                }

                # For DICTIONARY (excludes Node ID as it's the key)
                node_row_dict = {
                    'Hours_Flooded': hours_flooded,
                    'Maximum_Rate_CMS': max_rate,
                    'Time_of_Max_days': time_of_max_days,
                    'Time_of_Max_hr_min': time_of_max_hr_min,
                    'Total_Flood_Volume_10e6_ltr': total_flood_volume,
                    'Time_After_Raining_min': time_after_rain,
                    'Vulnerability_Category': vulnerability_category,
                    'Vulnerability_Score': vulnerability_score
                }

                all_nodes_array.append(node_row_array)
                all_nodes_dict[node_id] = node_row_dict

        print(f"Successfully processed {len(all_nodes_array)} total nodes")

    except Exception as e:
        print(f"Error processing OUT file: {e}")
        return json.dumps({"error": str(e), "nodes": [], "nodes_index": {}})

    # Summary statistics
    flooded_count = sum(1 for node in all_nodes_array if node['Hours_Flooded'] > 0)
    non_flooded_count = len(all_nodes_array) - flooded_count

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"{'='*60}")
    print(f"Total nodes: {len(all_nodes_array)}")
    print(f"Flooded nodes: {flooded_count}")
    print(f"Non-flooded nodes: {non_flooded_count}")
    print(f"{'='*60}")

    # Show sample of both flooded and non-flooded nodes
    print("\n📋 Sample of FLOODED nodes:")
    flooded_samples = [node for node in all_nodes_array if node['Hours_Flooded'] > 0][:3]
    if flooded_samples:
        for node in flooded_samples:
            print(f"  {node['Node']}: {node['Hours_Flooded']} hrs, {node['Maximum_Rate_CMS']} CMS, {node['Time_After_Raining_min']} min, {node['Vulnerability_Category']}")
    else:
        print("  No flooded nodes found")

    print("\n📋 Sample of NON-FLOODED nodes:")
    non_flooded_samples = [node for node in all_nodes_array if node['Hours_Flooded'] == 0][:3]
    if non_flooded_samples:
        for node in non_flooded_samples:
            print(f"  {node['Node']}: No flooding, {node['Vulnerability_Category']}")
    else:
        print("  All nodes flooded")

    # Create HYBRID JSON structure with both array and dictionary
    result = {
        "metadata": {
            "total_nodes": len(all_nodes_array),
            "flooded_nodes": flooded_count,
            "non_flooded_nodes": non_flooded_count,
            "rpt_file": rpt_file_path,
            "out_file": out_file_path,
            "model_file": model_path if kmeans is not None else "N/A",
            "structure_info": {
                "nodes_list": "Array format - use for iteration and listing all nodes",
                "nodes_dict": "Dictionary format - use for fast O(1) lookup by node ID"
            }
        },
        "nodes_list": all_nodes_array,        # Array format (with Node ID in each object)
        "nodes_dict": all_nodes_dict     # Dictionary format (Node ID as key)
    }

    # Convert to JSON string with proper formatting
    json_output = json.dumps(result, indent=2)

    return json_output