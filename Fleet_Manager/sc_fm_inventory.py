#!/usr/bin/env python3
import os
import requests
import json
import sys

# Define the API endpoint and organization ID
api_url = "https://api.scalecomputing.com/api/v2/clusters"
api_key = os.getenv("SC_FM_APIKEY")

# Check for missing API key
if not api_key:
    print("Error: SC_FM_APIKEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

# Headers for the API call
headers = {
    "x-api-key": api_key,
    "Accept": "application/json"
}

def fetch_clusters():
    url = f"{api_url}?limit=1000"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching clusters: {response.status_code}, {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()["items"]

def generate_inventory(clusters):
    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "children": []
        }
    }

    for cluster in clusters:
        cluster_name = cluster["name"]
        ip_address = cluster.get("leaderNodeLanIp", None)
        if not ip_address:
            print(f"Warning: Cluster {cluster_name} does not have a valid IP address.", file=sys.stderr)
            continue

        inventory["_meta"]["hostvars"][ip_address] = {
            "id": cluster["id"],
            "organizationId": cluster["organizationId"],
            "nodeCount": cluster["nodeCount"],
            "version": cluster["version"],
            "storagePercent": cluster["storagePercent"],
            "memoryPercent": cluster["memoryPercent"],
            "cpuPercent": cluster["cpuPercent"],
            "healthScore": cluster["healthScore"],
            "healthState": cluster["healthState"],
            "vmRunning": cluster["vmRunning"],
            "vmTotal": cluster["vmTotal"],
            "onlineStatus": cluster["onlineStatus"],
            "updatesAvailable": cluster["updatesAvailable"],
            "tags": cluster["tags"]
        }

        # Add the cluster group
        if cluster_name not in inventory:
            inventory[cluster_name] = {
                "hosts": []
            }

        inventory[cluster_name]["hosts"].append(ip_address)

    return inventory

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        clusters = fetch_clusters()
        inventory = generate_inventory(clusters)
        print(json.dumps(inventory, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        # --host can be used to get specific details of a host, though in this case it's redundant
        print(json.dumps({}, indent=2))
    else:
        print("Usage: --list | --host <hostname>", file=sys.stderr)
        sys.exit(1)