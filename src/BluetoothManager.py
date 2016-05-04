# BluetoothManager.py
# Written By: Abe Millan

import bluetooth

class BluetoothManager():
    def __init__(self):
        pass
    def deviceByName(self, blename):
        serviceMatches = bluetooth.find_service(name = blename)
        if len(service_matches) == 0:
            return -1
        firstMatch = service_matches[0]
        port = firstMatch["port"]
        name = firstMatch["name"]
        host = firstMatch["host"]

        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        try:
            sock.connect((host, port))
        except BluetoothException:
            return -2
        return sock
