# country-ip-block-generator
script to generate CIDR country-level IP data, straight from the Regional Internet Registries


A simple, fast, and fully transparent Python script that generates per-country IPv4 CIDR lists using official Regional Internet Registry (RIR) data.
This project is inspired by the approach used by Michael Herrbischoff and others—leveraging publicly available IP allocation data to build reliable country-based IP block lists.


Features:
Pulls Data from all major RIRs:
- ARIN
- RIPE NCC
- APNIC
- LACNIC
- AFRINIC

Generates per-country CIDR lists
Deduplicates and normalizes IP ranges
Atomic file writes (no partial/corrupt output)
Designed for automation (use cron/systemd)
Outputs plain text files for easy integration with Appliances such as Firewalls



How it works:
1) Downloads the latest delegated IP allocation files from each RIR
2) Parses IPv4 allocations by country
3) Converts IP ranges into CIDR blocks
4) Deduplicates and sorts results
5) Writes output files per country



By default, the script writes files to:
/var/www/ip-lists/

Which should be perfect for publishing your own private list to your own web server for you own use case.

Example:
/var/www/ip-lists/<Country_code.txt>

e.g:
US.txt
CA.txt
DE.txt


Requirements:
- Python 3.11+
- "requests" library

To install dependencies: "pip install requests"


Automation Example:
Run the script hourly using cron:
crontab -e
Add:
0 * * * * /usr/bin/python3 /path/to/generate_ip_lists.py


IMPORTANT NOTE:
IP Allocation does not mean the actual Physical Location is correct. These lists are based on RIR allocation data, not real-time geolocation.

- IPs may be used outside their registered country
- Cloud providers can skew results significantly
- This is not Suitable for High-Precision Geo Blocking

This is best used for:
Coarse filtering
Compliance use cases
Internal tooling

Not recommended for:
Fraud detection
Precise geolocation enforcement


Data Sources:
This project is using data publicly available from ARIN, RIPE NCC, APNIC, LACNIC, and AFRINIC
