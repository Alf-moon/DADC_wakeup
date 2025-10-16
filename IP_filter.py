import re
import subprocess

result = subprocess.run(['ip', 'a'], capture_output=True, text=True)
output = result.stdout
###
pattern = r'''
    ^(?P<num>\d+):\s+(?P<iface>\w+):\s+<.*?>\s+.*?
    .*?
    (?:link/ether\s+(?P<mac>[0-9a-fA-F:]{17})\s+brd.*?)?
    .*?
    (?:inet\s+(?P<ipv4>\d{1,3}(?:\.\d{1,3}){3})\/\d+\s+.*?)?
'''

matches = re.finditer(pattern, output, re.VERBOSE | re.DOTALL)

print("Available devices \n")

for match in matches:
    iface = match.group(1).strip()         
    mac = match.group(2)                    
    ip = match.group(3)                     

    print(f"Device: {iface}")
    if mac:
        print(f"  MAC Address: {mac}")
    if ip:
        print(f"  IPv4 地址: {ip}")
    print()