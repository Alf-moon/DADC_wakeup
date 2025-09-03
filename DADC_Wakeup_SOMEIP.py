import socket

def build_someip_packet(service_id, method_id, client_id, session_id, payload_bytes):
    protocol_version = 0x01
    interface_version = 0x01
    message_type = 0x00  # REQUEST
    return_code = 0x00

    # SOME/IP Length = 8字节头部 + payload长度（不含Length字段本身）
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

def send_someip_wakeup_udp(target_ip, target_port):
    # 参数配置（根据你的 ECU 协议定义）
    service_id = 0x0017
    method_id = 0x0001
    client_id = 0x0001
    session_id = 0x0001

    # 唤醒 Payload（示例数据，请根据实际协议替换）
    payload_hex = "00 04 08 05 10 00"
    payload_bytes = bytes.fromhex(payload_hex)

    # 构造 SOME/IP 报文
    packet = build_someip_packet(service_id, method_id, client_id, session_id, payload_bytes)

    # 创建 UDP 套接字并发送
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('100.64.10.100', 20023))  # 12345为你想要的源端口
    sock.sendto(packet, (target_ip, target_port))
    sock.close()

    print(f"✅ 唤醒帧已发送至 {target_ip}:{target_port}")

if __name__ == "__main__":
    # 替换为你的 ECU IP 和端口
    ecu_ip = "100.64.10.7"
    ecu_port = 20023

    send_someip_wakeup_udp(ecu_ip, ecu_port)
