import socket
import os
import argparse

from dotenv import load_dotenv
from hetznerAPI import update_hetzner_dns_record, print_hetzner_dns_record

# File keeping track of last change to IP
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

# Main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='dynDNS.py')
    parser.add_argument('-p', '--dnsprint', action='store_true', help='query and print all of your Hetzner DNS records')
    args = parser.parse_args()

    load_dotenv()

    hetzner_api_token = os.getenv('HETZNER_API_TOKEN')
    if not hetzner_api_token:
        print("No API Key. Please follow the README for instructions.")
        exit(1)
    if args.dnsprint:
        print_hetzner_dns_record(hetzner_api_token)
    else:
        domain = os.getenv('DOMAIN')
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