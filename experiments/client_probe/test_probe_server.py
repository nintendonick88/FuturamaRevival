import http.client
import io
import json
import threading
import unittest
from http.server import ThreadingHTTPServer

from probe_server import RequestRecorder, make_handler


class ProbeServerTests(unittest.TestCase):
    def test_records_request_and_returns_controlled_response(self) -> None:
        captured = io.BytesIO()
        recorder = RequestRecorder(captured)
        handler = make_handler(
            recorder,
            response_body=b'{"probe":true}',
            response_status=418,
            response_headers=(("X-Test-Evidence", "present"),),
        )
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            connection = http.client.HTTPConnection(*server.server_address)
            connection.request(
                "POST",
                "/tapservice/api/?test=1",
                body=b'{"hello":"world"}',
                headers={"Content-Type": "application/json"},
            )
            response = connection.getresponse()
            self.assertEqual(418, response.status)
            self.assertEqual("1", response.getheader("X-Futurama-Preservation-Probe"))
            self.assertEqual("present", response.getheader("X-Test-Evidence"))
            self.assertEqual(b'{"probe":true}', response.read())
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        event = json.loads(captured.getvalue())
        self.assertEqual("POST", event["method"])
        self.assertEqual("/tapservice/api/?test=1", event["path"])
        self.assertEqual('{"hello":"world"}', event["body_utf8"])
        self.assertEqual(17, event["body_length"])


if __name__ == "__main__":
    unittest.main()
