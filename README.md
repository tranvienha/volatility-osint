# Volatility OSINT plugin

OSINT plug-in allows incident handler quickly identify potential malicious processes by submitting  urls & ip addresses to open source intelligence platforms. It currently supports :
- http://sitereview.bluecoat.com
- https://www.virustotal.com
- http://www.misp-project.org/ :  Malware Information Sharing Platform (If necessary I can setup an online MISP for testing purpose)

Returned result could also help incident handler to have an idea about the attack ( targeted or not ), about profile of attacker and relation with pass incidents.

In order to 
- avoid to leak information
- avoid to expose our identity
- bypass request rate limitation of some intellignce platforms

We decide that
- Dumped files are not summited, only urls & ips
- Requests are sent through Tor proxy ( for Bluecoat & VirusTotal )

## Requirements
- Tor proxy
- pip install PySocks
- pip install requests

### Usage

This readme uses memory sample which can be downloaded from https://github.com/ganboing/malwarecookbook/tree/master/zeusscan

osint plug-in has the following command line parameters

| Name | Default value | Description |
| --- | --- | --- |
| --whitelist-file | whitelist.txt  |Domains, ip addresses in this file will be ignored |
| --socks5-host | 127.0.0.1 | Tor proxy ip address |
| --socks5-port | 9050 | Tor proxy port |
| --check-type | url| Submit urls or ip addresses |

Other parameters are defined in configuration file

| Name | value | Description |
| --- | --- | --- |
| SITEREVIEW_URL | http://sitereview.bluecoat.com/rest/categorization | RESTApi URL |
| VIRUSTOTAL_URL | https://www.virustotal.com/vtapi/v2/url/report | RESTApi URL |
| VIRUSTOTAL_TOKEN | Depends on your account | Authentication token |
| MISP_URL | Depends on your installation | RESTApi URL | 
| MISP_TOKEN | Depends on your account | Authentication token |

#### Submit urls

OSINT plug-in uses yarascan plug-in to extract urls from memory then submits them ( if not whitelisted ) to Bluecoat/VirusTotal/MISP

python vol.py –conf-file=./osint.conf -f zeus2x4.vmem osint

![Alt text](/osint_zeus2x4_domain.png?raw=true)

#### Submit ips

For ips, yarascan plug-in is not used because of too much false positive. OSINT uses connscan/netscan instead.

python vol.py –conf-file=./osint.conf -f zeus2x4.vmem osint –check-type=ip

![Alt text](/osint_zeus2x4_ip.png?raw=true)

#### Output Interpretation

The output has 5 columns : 
- Owner : Process in which url/ip extracted
- Bluecoat : Category of url/ip submitted
  - Malicious Sources/Malnets
  - Suspicious
  - …
- VirusTotal : 
  - Not Found – No one has submitted this url/ip
  - 2/65 – url/ip has been checked by someone and 2 AV detected it as malicious ( on total of 65 AV )
- MISP : 
  - Not Found – url/ip is not in IOC database. 
  - 1000 – this url/ip has been found in event with id=1000

Sometimes, "Error" value can be found in Bluecoat, VirusTotal or MISP columns because of: 
- Connection error
- url/ip is not valid
- request rate limit reached
- …
