import json
import unittest

from neomind.protocol import decode_message, encode_command, make_message


class ProtocolTests(unittest.TestCase):
    def test_encode_command_is_newline_delimited_json(self):
        raw = encode_command(7, "status", verbose=True)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertEqual(json.loads(raw), {
            "id": 7,
            "cmd": "status",
            "verbose": True,
        })

    def test_decode_message_accepts_bytes(self):
        self.assertEqual(decode_message(b'{"id":2,"ok":true}'), {
            "id": 2,
            "ok": True,
        })

    def test_decode_rejects_non_object(self):
        with self.assertRaises(ValueError):
            decode_message("[1, 2, 3]")

    def test_decode_rejects_invalid_json(self):
        with self.assertRaises(ValueError):
            decode_message("{broken")

    def test_command_rejects_newlines(self):
        with self.assertRaises(ValueError):
            encode_command(1, "bad\ncommand")

    def test_make_message(self):
        message = make_message("abc", "set_led", value=1)
        self.assertEqual(message.message_id, "abc")
        self.assertEqual(message.payload, {"value": 1})


if __name__ == "__main__":
    unittest.main()
