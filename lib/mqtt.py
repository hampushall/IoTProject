import usocket as socket
import ustruct as struct
from ubinascii import hexlify
import utime

class MQTTException(Exception):
    pass

class MQTTClient:

    # ... [other methods remain unchanged]

    def wait_msg(self):
        try:
            res = self.sock.read(1)
            self.sock.setblocking(True)
            if res is None:
                return None
            if res == b"":
                raise OSError(-1)
            if res == b"\xd0":  # PINGRESP
                sz = self.sock.read(1)[0]
                assert sz == 0
                return None
            op = res[0]
            if op & 0xf0 != 0x30:
                return op
            sz = self._recv_len()
            topic_len = self.sock.read(2)
            topic_len = (topic_len[0] << 8) | topic_len[1]
            topic = self.sock.read(topic_len)
            sz -= topic_len + 2
            if op & 6:
                pid = self.sock.read(2)
                pid = pid[0] << 8 | pid[1]
                sz -= 2
            msg = self.sock.read(sz)
            self.cb(topic, msg)
            if op & 6 == 2:
                pkt = bytearray(b"\x40\x02\0\0")
                struct.pack_into("!H", pkt, 2, pid)
                self.sock.write(pkt)
            elif op & 6 == 4:
                assert 0
        except OSError as e:
            if e.errno == -1:
                print("OSError -1 encountered: possible network issue or broker not responding.")
                self.reconnect()
            else:
                raise e

    def check_msg(self):
        self.sock.setblocking(False)
        return self.wait_msg()

    def reconnect(self):
        print("Attempting to reconnect...")
        self.sock.close()
        utime.sleep(5)  # Wait before reconnecting
        self.connect()

# Usage example with error handling and logging

def main():
    mqtt_client = MQTTClient(client_id="client_id", server="broker_address", user="username", password="password")
    mqtt_client.set_callback(lambda topic, msg: print(f"Received message on topic {topic}: {msg}"))
    try:
        mqtt_client.connect()
        mqtt_client.subscribe("test/topic")
        while True:
            mqtt_client.check_msg()
            utime.sleep(1)
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
