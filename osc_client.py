from pythonosc import udp_client

class OscClient:

    def __init__(self, ip = "127.0.0.1", port = 7400):
        self.ip = ip
        self.port = port
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)
        print(f"connection... ip: {self.ip}, port: {self.port}")

    def send_message(self, atr, message):
        self.client.send_message(atr, message)
        print(f"sending... {atr}/{message}")
