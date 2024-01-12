import requests

# Method that posts the given IP to the target dns record
def update_hetzner_dns_record(api_token, record_id, ip_address, zone_id):
    """Update DNS record in Hetzner."""
    url = f"https://dns.hetzner.com/api/v1/records/{record_id}"
    headers = {
        "Auth-API-Token": api_token,
        "Content-Type": "application/json"
    }
    data = {
        "zone_id": zone_id,
        "type": "A",
        "name": "home",
        "value": ip_address,
        "ttl": 0
    }
    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating DNS record: {e}")
        return None
    
# Method to print all dns zones and their records
def print_hetzner_dns_record(api_token):
    """Print all Hetzner DNS records."""
    url = f"https://dns.hetzner.com/api/v1/zones"
    headers = {
        "Auth-API-Token": api_token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        for zcnt, zone in enumerate(response.json()["zones"]):
            print("Zone " + str(zcnt+1), "(name=" + zone["name"] + ",", "id=" + zone["id"] + ")")

            url="https://dns.hetzner.com/api/v1/records"
            params={"zone_id": zone["id"]}
            response2 = requests.get(url, params=params, headers=headers)
            response2.raise_for_status()  # Raises an HTTPError for bad responses

            for rcnt, record in enumerate(response2.json()["records"]):
                print("\tRecord " + str(rcnt+1), 
                      "(type=" + record["type"] + ",", 
                      "name=" + record["name"] + ",", 
                      "value=" + (record["value"][:18] + '..') if len(record["value"]) > 18 else record["value"] + ",", 
                      "id=" + record["id"] + ")")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DNS zones: {e}")