import pandas as pd
from pyswmm import Output, NodeSeries
import json

def get_node_flooding_summary(rpt_file_path, out_file_path):
    """
    Convert Node Flooding Summary from RPT file to JSON format with hybrid structure.
    Includes all nodes from OUT file, with 0 values for non-flooded nodes.

    Args:
        rpt_file_path: Path to the input .rpt file
        out_file_path: Path to the input .out file

    Returns:
        str: JSON string containing all nodes with flooding summary data in hybrid structure
    """

    # Read the RPT file
    with open(rpt_file_path, 'r') as file:
        content = file.read()

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

            flooded_nodes_data[node] = {
                'Hours Flooded': parts[1],
                'Maximum Rate (CMS)': parts[2],
                'Time of Max (days)': parts[3],
                'Time of Max (hr:min)': parts[4],
                'Total Flood Volume (10^6 ltr)': parts[5],
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
                    # For ARRAY (includes Node ID)
                    node_row_array = {
                        'Node': node_id,
                        'Hours_Flooded': float(flooded_nodes_data[node_id]['Hours Flooded']),
                        'Maximum_Rate_CMS': float(flooded_nodes_data[node_id]['Maximum Rate (CMS)']),
                        'Time_of_Max_days': float(flooded_nodes_data[node_id]['Time of Max (days)']),
                        'Time_of_Max_hr_min': flooded_nodes_data[node_id]['Time of Max (hr:min)'],
                        'Total_Flood_Volume_10e6_ltr': float(flooded_nodes_data[node_id]['Total Flood Volume (10^6 ltr)']),
                        'Time_After_Raining_min': float(minutes_after_rain)
                    }

                    # For DICTIONARY (excludes Node ID as it's the key)
                    node_row_dict = {
                        'Hours_Flooded': float(flooded_nodes_data[node_id]['Hours Flooded']),
                        'Maximum_Rate_CMS': float(flooded_nodes_data[node_id]['Maximum Rate (CMS)']),
                        'Time_of_Max_days': float(flooded_nodes_data[node_id]['Time of Max (days)']),
                        'Time_of_Max_hr_min': flooded_nodes_data[node_id]['Time of Max (hr:min)'],
                        'Total_Flood_Volume_10e6_ltr': float(flooded_nodes_data[node_id]['Total Flood Volume (10^6 ltr)']),
                        'Time_After_Raining_min': float(minutes_after_rain)
                    }
                else:
                    # Node did not flood - all values are 0
                    # For ARRAY
                    node_row_array = {
                        'Node': node_id,
                        'Hours_Flooded': 0.0,
                        'Maximum_Rate_CMS': 0.0,
                        'Time_of_Max_days': 0.0,
                        'Time_of_Max_hr_min': '0:00',
                        'Total_Flood_Volume_10e6_ltr': 0.0,
                        'Time_After_Raining_min': 0.0
                    }

                    # For DICTIONARY
                    node_row_dict = {
                        'Hours_Flooded': 0.0,
                        'Maximum_Rate_CMS': 0.0,
                        'Time_of_Max_days': 0.0,
                        'Time_of_Max_hr_min': '0:00',
                        'Total_Flood_Volume_10e6_ltr': 0.0,
                        'Time_After_Raining_min': 0.0
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

    # Create HYBRID JSON structure with both array and dictionary
    result = {
        "metadata": {
            "total_nodes": len(all_nodes_array),
            "flooded_nodes": flooded_count,
            "non_flooded_nodes": non_flooded_count,
            "rpt_file": rpt_file_path,
            "out_file": out_file_path,
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

