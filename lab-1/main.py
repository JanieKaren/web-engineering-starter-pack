""""
CMSC 126 - Web Engineering B2
Lab Activity 1
Simulating the OSI Model from Scratch in Python
Partners: 
    Cerio, Kristine Faye ⋆˚✿˖°
    de Pedro, Janie Karen ⋆˚✿˖°

"""
import threading
from layers import ApplicationLayer, PresentationLayer, SessionLayer, TransportLayer, NetworkLayer, DataLinkLayer, PhysicalLayer

class Server:
    def __init__(self, host, port, event):
        self.physical_layer = PhysicalLayer(host, port, is_server=True)  
        self.datalink_layer = DataLinkLayer(mac_address="AA:BB:CC:DD:EE:00")
        self.network_layer = NetworkLayer(ip_address="192.168.10.11")
        self.transport_layer = TransportLayer()
        self.session_layer = SessionLayer()
        self.presentation_layer = PresentationLayer()
        self.application_layer = ApplicationLayer()
        self.event = event

    def start(self):
        print("────୨ৎ────Server started...────୨ৎ────")
        self.event.set() 

        data = self.physical_layer.receive()  
        print(f"Physical Layer: Received Data: {data}")

        if data:
            data = self.datalink_layer.unframe_data(data)
            print("Data Link Layer: Unframed Data:", data)

            data = self.network_layer.depacketize(data)
            print("Network Layer: Depacketized Data:", data)

            data = self.transport_layer.reassemble_data(data)
            print("Transport Layer: Reassembled Data:", data)

            data = self.presentation_layer.decode_data(data)
            print("Presentation Layer: Decoded Data:", data)

            decoded_data = self.application_layer.decode_request(data)
            print("Application Layer: Received Request:", decoded_data)

            
            self.session_layer.close_session()


class Client:
    def __init__(self, host, port, event):
        self.physical_layer = PhysicalLayer(host, port, is_server=False) 
        self.datalink_layer = DataLinkLayer(mac_address="00:EE:DD:CC:BB:AA")
        self.network_layer = NetworkLayer(ip_address="192.168.10.2")
        self.transport_layer = TransportLayer()
        self.session_layer = SessionLayer()
        self.presentation_layer = PresentationLayer()
        self.application_layer = ApplicationLayer()
        self.event = event

    def start(self):
        self.event.wait() 
        self.session_layer.open_session()

        data = self.application_layer.create_request("Hello from client ⸜(｡˃ ᵕ ˂ )⸝♡")
        print("Application Layer: Created Request:", data.decode())

        data = self.presentation_layer.encode_data(data)
        print("Presentation Layer: Encoded Data:", data)

        data = self.transport_layer.segment_data(data)
        print("Transport Layer: Segmented Data:", data)

        data = self.network_layer.packetize(data)
        print("Network Layer: Packetized Data:", data)

        data = self.datalink_layer.frame_data(data)
        print("Data Link Layer: Framed Data:", data)


        self.physical_layer.send(data)  
        self.session_layer.close_session()

# Run simulation
host = 'localhost'
port = 55545

event = threading.Event() 

server = Server(host, port, event)
client = Client(host, port, event)

server_thread = threading.Thread(target=server.start)
client_thread = threading.Thread(target=client.start)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()

