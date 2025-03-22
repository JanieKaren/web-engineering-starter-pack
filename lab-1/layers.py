import socket
import struct
import base64
import json

# Physical Layer: Simulated using Python sockets and bit-level operations.
class PhysicalLayer:
    def __init__(self, host, port, is_server=False):
        self.host = host
        self.port = port
        self.is_server = is_server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.is_server:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"Server listening on {self.host}:{self.port}")
        else:
            self.socket.connect((self.host, self.port))

    def send(self, data):
        if not self.is_server:  
            self.socket.sendall(data)
        else:
            self.client_socket.sendall(data)  

    def receive(self):
        if not self.is_server:
            raise RuntimeError("Receive should only be called on the server! Naur")

        self.client_socket, addr = self.socket.accept()
        print(f"Connection established with {addr}")
        data = self.client_socket.recv(1024)
        return data


# Data Link Layer: Implements a MAC addressing system and frame transmission.
class DataLinkLayer:
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def frame_data(self, data):
        frame = struct.pack("!6s", self.mac_address.encode()) + data
        return frame

    def unframe_data(self, frame):
        mac_address = struct.unpack("!6s", frame[:6])[0].decode()
        data = frame[6:]
        return data
    
# Network Layer: Simulates IP addressing and packet routing.
class NetworkLayer:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def packetize(self, data):
        packet = struct.pack("!4s", self.ip_address.encode()) + data
        return packet

    def depacketize(self, packet):
        ip_address = struct.unpack("!4s", packet[:4])[0].decode()
        data = packet[4:]
        return data

# Transport Layer: Implements TCP-like packet sequencing and error handling.
class TransportLayer:
    def __init__(self):
        self.sequence_number = 0

    def segment_data(self, data):
        segment = struct.pack("!I", self.sequence_number) + data
        self.sequence_number += 1
        return segment

    def reassemble_data(self, segment):
        sequence_number = struct.unpack("!I", segment[:4])[0]
        data = segment[4:]
        return data
    
# Session Layer: Manages connection states and synchronization.
class SessionLayer:
    def __init__(self):
        self.session_state = "CLOSED"

    def open_session(self):
        self.session_state = "OPEN"
        print("────୨ৎ────Session opened....────୨ৎ────")

    def close_session(self):
        self.session_state = "CLOSED"
        print("Session closed....Buh-bye!(╥﹏╥)")

    def get_session_state(self):
        return self.session_state

# Presentation Layer: Handles encryption, compression, and encoding.
class PresentationLayer:
    def __init__(self):
        pass

    def encode_data(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8') 
        encoded_data = base64.b64encode(data)
        return encoded_data

    def decode_data(self, data):
        # Decode the base64 data
        decoded_data = base64.b64decode(data)
        return decoded_data
    
# Application Layer: Implements HTTP-like request-response communication.
class ApplicationLayer:
    def __init__(self):
        pass

    def create_request(self, data):
        request = json.dumps({"request": data}, ensure_ascii=False)
        return request.encode()

    def decode_request(self, request):
        data = json.loads(request.decode())["request"]
        return data

    def send_response(self, data):
        response = json.dumps({"response": data})
        return response.encode()

    def decode_response(self, response):
        data = json.loads(response.decode())["response"]
        return data
    

