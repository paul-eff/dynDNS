import socket
import requests
import os

from dotenv import load_dotenv

# File keeping track of last changed to IP
ip_file = 'last_ip.txt'

# Method that resolved domain to IP and determines if it changed
def resolve_ip_address(domain):
    """Resolve IP address for a given domain."""
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"Error resolving IP for {domain}: {e}")
        return None
    if not os.path.exists(ip_file):
        with open(ip_file, 'w+') as f:
            pass
    with open(ip_file, 'r') as f:
        lines = f.readlines()
    if len(lines) > 0:
        if ip in lines[0]:
            print(f'IP did not change. Still {ip}')
            return None
    return ip
        
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

# Main method
if __name__ == "__main__":
    load_dotenv()

    domain = os.getenv('DOMAIN')
    hetzner_api_token = os.getenv('HETZNER_API_TOKEN')
    dns_record_id = os.getenv('DNS_RECORD_ID')
    dns_record_zone_id = os.getenv('DNS_RECORD_ZONE_ID')

    ip_address = resolve_ip_address(domain)
    if ip_address:
        response = update_hetzner_dns_record(hetzner_api_token, dns_record_id, ip_address, dns_record_zone_id)
        if response:
            print(f'IP changed to {ip_address}')
            with open (ip_file, 'w') as f:
                f.writelines([ip_address])
            print("DNS record updated successfully:", response)
        else:
            print("Failed to update DNS record.")
