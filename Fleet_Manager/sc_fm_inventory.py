#!/usr/bin/env python3
import os
import requests
import json
import sys
from typing import Any, Dict, List

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

DEFAULT_TIMEOUT_SECONDS = float(os.getenv("SC_FM_TIMEOUT", "15"))

def fetch_clusters() -> List[Dict[str, Any]]:
    """
    Fetch cluster list from Fleet Manager.
    Adds a timeout and handles request/JSON errors to avoid hanging inventory calls.
    """
    url = f"{api_url}?limit=1000"
    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT_SECONDS)
    except requests.exceptions.RequestException as exc:
        print(f"Error fetching clusters: {exc}", file=sys.stderr)
        sys.exit(1)

    if response.status_code != 200:
        print(f"Error fetching clusters: {response.status_code}, {response.text}", file=sys.stderr)
        sys.exit(1)

    try:
        payload = response.json()
    except ValueError as exc:
        print(f"Error decoding JSON response: {exc}", file=sys.stderr)
        sys.exit(1)

    items = payload.get("items")
    if not isinstance(items, list):
        print("Error: API response missing 'items' list.", file=sys.stderr)
        sys.exit(1)

    return items

def generate_inventory(clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
    inventory: Dict[str, Any] = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "children": []
        }
    }

    children = set()
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
        children.add(cluster_name)

    inventory["all"]["children"] = sorted(children)
    return inventory

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        clusters = fetch_clusters()
        inventory = generate_inventory(clusters)
        print(json.dumps(inventory, indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == "--host":
        # Return hostvars for a single host. Ansible typically passes the inventory hostname here.
        host = sys.argv[2]
        clusters = fetch_clusters()
        inventory = generate_inventory(clusters)
        hostvars = inventory.get("_meta", {}).get("hostvars", {})
        print(json.dumps(hostvars.get(host, {}), indent=2))
    else:
        print("Usage: --list | --host <hostname>", file=sys.stderr)
        sys.exit(1)