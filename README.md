# dynDNS v0.9
<p align="center">
  <img src="https://img.shields.io/badge/version-0.9-green">
  <img src="https://img.shields.io/badge/python-3.11.4-yellow">
</p>

My ISP only provides me with a non-static IPv4 address. Getting a static one would cost hella extra and I really do not want to pay a dynamic DNS service monthly...

I automated the task by calling a URL that my FritzBox provides via MyFritz (to retrieve its current IP), and then update the DNS record in Hetzner.

**Important**: If your router does not provide a service similar to my FritzBox, I am currently working on an offline mode so your device running the script can fetch the IP from the local network.

# Usage

- [Clone the project](#development) to the system where you want to have this running (I have it on a Hetzner server).
- Rename `.template.env` to `.env` and fill in the missing fields
  - **DOMAIN**: You need a URL that can be resolved to your router's current non-static IP. I was using a FritzBox, which provides the MyFritz service. When enabled the FritzBox then provides me with said URL. [Learn more...](https://en.avm.de/service/knowledge-base/dok/FRITZ-Box-7590-AX/1018_Determining-the-MyFRITZ-address-to-directly-access-FRITZ-Box-and-home-network-from-the-internet/)
  - **HETZNER_API_TOKEN**: Look at [this guide](https://docs.hetzner.com/dns-console/dns/general/api-access-token/) to create a Hetzner DNS API token.
  - **DNS_RECORD_ID** & **DNS_RECORD_ZONE_ID**: Acquired via the script itself by using the `-p` argument.
- Create a cronjob, or any  other automation, that executes the following command
```zsh
python3 dynDNS.py
```
- The `-p` argument will print your DNS record and record zone IDs.
- `--offline` is WIP. This argument will retrieve the IP from the local network, e.g. for people whos router does not provide any MyFritz similar service.
- When given no argument, the script will update your DNS record with the current IP.

# Development
Make sure you have `python3` and the `pipenv` package installed.

Clone the project to your local system with e.g.
```zsh
git clone git@github.com:paul-eff/dynDNS.git
```

Navigate into the folder and execute the command 
```zsh
pipenv shell
```

Pipenv will now install all dependencies. From here on out you can change the code as you wish.  
When finished, type `exit` to leave the environment.

# Reminder

If you need this script e.g. in another language or something else, please leave me a message or issue :)!
