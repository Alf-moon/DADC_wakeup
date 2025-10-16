import socket
import os
import subprocess
import re
import time

def set_nic_config():
    pattern = re.compile(r'100\.64\.10\.\d{1,3}')
    print(os.name)
    if os.name ==  "posix":
        nic_config_raw = subprocess.run(['ifconfig'], capture_output=True, text=True)
        for line in nic_config_raw.stdout.splitlines():
            if pattern.search(line):
                print("Correct IP has been set up!")
                return
            
        print("No proper IP has been set, will set up the link!")
        subprocess.run(
            ['sudo', 'ip', 'link', 'add', 'dev', 'eth0.10', 'link', 'eth0', 'type', 'vlan', 'id', '10'], 
            capture_output=True, 
            text=True
        )
        subprocess.run(
            ['sudo', 'ip', 'addr', 'add', '100.64.10.15/24', 'dev', 'eth0.10'], 
            capture_output=True, 
            text=True
        )
        subprocess.run(
            ['sudo', 'ip', 'link', 'set', 'up', 'eth0.10'], 
            capture_output=True, 
            text=True
        )
    
    # There is bug in this elif block!!!
    elif os.name == "nt":
        nic_config_raw = subprocess.run(
            ["powershell", "-Command", "ipconfig"],
            capture_output=True, 
            text=True
        )
        
        for line in nic_config_raw.stdout.splitlines():
            if pattern.search(line):
                print("Correct IP has been set up!")
                return
            
        print("No proper IP has been set, will set up the link!")
        subprocess.run(
            ["powershell", "-Command", 'Set-NetAdapter -Name "eth0" -VlanID 10'], 
            capture_output=True, 
            text=True
        )
        subprocess.run(
            ["powershell", "-Command", 'New-NetIPAddress -InterfaceAlias "eth0" -IPAddress "100.64.10.15" -PrefixLength 24 -DefaultGateway "100.64.10.1"'], 
            capture_output=True, 
            text=True
        )

def build_someip_packet(service_id, method_id, client_id, session_id, payload_bytes):
    protocol_version = 0x01
    interface_version = 0x01
    message_type = 0x00  # REQUEST
    return_code = 0x00

    # SOME/IP Length = 8 Bytes Header + payload length
    length = 8 + len(payload_bytes)

    header = (
        service_id.to_bytes(2, 'big') +
        method_id.to_bytes(2, 'big') +
        length.to_bytes(4, 'big') +
        client_id.to_bytes(2, 'big') +
        session_id.to_bytes(2, 'big') +
        protocol_version.to_bytes(1, 'big') +
        interface_version.to_bytes(1, 'big') +
        message_type.to_bytes(1, 'big') +
        return_code.to_bytes(1, 'big')
    )

    return header + payload_bytes

# UDP sending function
def send_someip_wakeup_udp(target_ip, target_port):
    service_id = 0x0017
    method_id = 0x0001
    client_id = 0x0001
    session_id = 0x0001

    # Payload definition
    payload_hex = "00 04 08 05 10 00"
    payload_bytes = bytes.fromhex(payload_hex)

    # SOME/IP packet building
    packet = build_someip_packet(service_id, method_id, client_id, session_id, payload_bytes)

    # Create UDP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('100.64.10.15', 20023)) 
        sock.sendto(packet, (target_ip, target_port))
        sock.close()
    except OSError as e:
        print(f"❌ Failed to bind socket: {e}")
        return
    
    print(f"✅ Wakeup frame has been sent to {target_ip}:{target_port}")

if __name__ == "__main__":
    ecu_ip = "100.64.10.7"
    ecu_port = 20023
    set_nic_config()
    send_someip_wakeup_udp(ecu_ip, ecu_port)
