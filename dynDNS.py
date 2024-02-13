import socket
import os
import argparse
import requests

from dotenv import load_dotenv
from hetznerAPI import update_hetzner_dns_record, print_hetzner_dns_record

# File keeping track of last IP
ip_file = None

# Method that resolves domain to IP
def resolve_ip_address(domain):
    """Resolve IP address for a given domain."""
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"Error resolving IP for {domain}: {e}")
        return None
    return ip

# Method that determined your public IP from the current network
def get_ip_from_local():
    """Retrieve public IP from the current network."""
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to retrieve public IP:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error:", e)
        return None


# Main method
if __name__ == "__main__":
    # Create args parser
    parser = argparse.ArgumentParser(prog='dynDNS.py')
    parser.add_argument('-p', '--dnsprint', action='store_true', help='query and print all of your Hetzner DNS records')
    parser.add_argument('-l', '--local', action='store_true', help='retrieve your IP address from the current network')
    args = parser.parse_args()

    load_dotenv()

    hetzner_api_token = os.getenv('HETZNER_API_TOKEN')
    # Check for API key
    if not hetzner_api_token:
        print("No API key. Please follow the README for instructions.")
    # Print Hetzner DNS records
    elif args.dnsprint:
        print_hetzner_dns_record(hetzner_api_token)
    # Update Hetzner DNS record
    else:
        domain = os.getenv('DOMAIN')
        dns_record_id = os.getenv('DNS_RECORD_ID')
        dns_record_zone_id = os.getenv('DNS_RECORD_ZONE_ID')
        ip_file = os.getenv('IP_FILE')
        # Make sure the file exists
        if not os.path.exists(ip_file):
            with open(ip_file, 'w+') as f:
                pass
        # Get IP address depending on the flag
        ip_address = get_ip_from_local() if args.local else resolve_ip_address(domain)
        if ip_address:
            # Update the DNS record
            response = update_hetzner_dns_record(hetzner_api_token, dns_record_id, ip_address, dns_record_zone_id)
            # If successfull, print and update file. If not, print error
            if response:
                print("DNS record updated successfully:", response)
                with open(ip_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        if ip_address in lines[0]:
                            print(f'IP did not change. Still {ip_address}')
                        else:
                            print(f'IP changed to {ip_address}')
                with open (ip_file, 'w') as f:
                    f.writelines([ip_address])
            else:
                print("Failed to update DNS record.")