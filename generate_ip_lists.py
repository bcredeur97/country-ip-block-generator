import requests
import ipaddress
from collections import defaultdict
from datetime import datetime, UTC
import os
import tempfile
import shutil

RIR_URLS = [
    "https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest",
    "https://ftp.apnic.net/pub/stats/apnic/delegated-apnic-latest",
    "https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest",
    "https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest",
    "https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest"
]

OUTPUT_DIR = "/var/www/iplists"

def fetch_data():
    lines = []
    for url in RIR_URLS:
        print(f"Fetching {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        lines.extend(r.text.splitlines())
    return lines

def parse_data(lines):
    country_map = defaultdict(set)

    for line in lines:
        if line.startswith("#") or "|" not in line:
            continue

        parts = line.split("|")
        if len(parts) < 7:
            continue

        _, country, ip_type, start, value, *_ = parts

        if ip_type != "ipv4":
            continue

        try:
            count = int(value)
            start_ip = ipaddress.IPv4Address(start)
            end_ip = start_ip + count - 1

            for net in ipaddress.summarize_address_range(start_ip, end_ip):
                country_map[country].add(str(net))

        except Exception:
            continue

    return country_map

def atomic_write(filepath, content):
    dir_name = os.path.dirname(filepath)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name) as tmp:
        tmp.write(content)
        temp_name = tmp.name

    shutil.move(temp_name, filepath)

def write_output(country_map):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for country, nets in country_map.items():
        path = os.path.join(OUTPUT_DIR, f"{country}.txt")
        content = "\n".join(sorted(nets))
        atomic_write(path, content)

    # timestamp file
    atomic_write(
        os.path.join(OUTPUT_DIR, "last_updated.txt"),
        datetime.now(UTC).isoformat()
    )

def main():
    lines = fetch_data()
    country_map = parse_data(lines)
    write_output(country_map)

if __name__ == "__main__":
    main()
