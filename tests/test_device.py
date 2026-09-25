import unittest
from neomind.device import NeoMindDevice

class FakeRuntime:
    def __init__(self): self.calls = []
    def request(self, message_id, command, **payload):
        self.calls.append((message_id, command, payload)); return {"id": message_id, "ok": True}

class DeviceTests(unittest.TestCase):
    def test_device_commands_map_to_protocol(self):
        runtime = FakeRuntime(); device = NeoMindDevice(runtime)
        device.ping("p"); device.status("s"); device.set_led(True, "l")
        self.assertEqual(runtime.calls, [("p", "ping", {}), ("s", "status", {}), ("l", "set_led", {"value": True})])

if __name__ == "__main__": unittest.main()
