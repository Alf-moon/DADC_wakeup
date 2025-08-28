import socket

def send_wakeup_frame(interface, dst_mac, src_mac, eth_type, payload):
    # 构造以太网帧
    # 构造 SOME/IP 协议头部
    # 参考SOME/IP协议，基本头部为16字节
    # Service ID (2字节), Method ID (2字节), Length (4字节), Client ID (2字节), Session ID (2字节), Protocol Version (1字节), Interface Version (1字节), Message Type (1字节), Return Code (1字节)
    service_id = 0x0017
    method_id = 0x0001
    client_id = 0x0001
    session_id = 0x0001
    protocol_version = 0x01
    interface_version = 0x01
    message_type = 0x00  # REQUEST
    return_code = 0x00

    # SOME/IP数据长度 = 剩余字节数（不含前4字节Length本身）
    someip_payload = payload
    someip_length = 8 + len(someip_payload)  # 剩余字段+数据

    someip_header = (
        service_id.to_bytes(2, 'big') +
        method_id.to_bytes(2, 'big') +
        someip_length.to_bytes(4, 'big') +
        client_id.to_bytes(2, 'big') +
        session_id.to_bytes(2, 'big') +
        protocol_version.to_bytes(1, 'big') +
        interface_version.to_bytes(1, 'big') +
        message_type.to_bytes(1, 'big') +
        return_code.to_bytes(1, 'big')
    )

    someip_frame = someip_header + someip_payload

    frame = bytes.fromhex(dst_mac.replace(':', '')) + \
            bytes.fromhex(src_mac.replace(':', '')) + \
            eth_type.to_bytes(2, byteorder='big') + \
            someip_frame

    # 创建原始套接字
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface, 0))
    s.send(frame)
    s.close()

if __name__ == "__main__":
    interface = "enp0s31f6"  # 替换为你的网卡名
    dst_mac = "48:d3:5d:00:12:94"  # 目标MAC地址
    src_mac = "ac:91:a1:10:88:98"  # 源MAC地址
    eth_type = 0x0800  # 以太网类型（IPv4）
    payload = 0x000408051000  # 你的数据

    send_wakeup_frame(interface, dst_mac, src_mac, eth_type, payload)