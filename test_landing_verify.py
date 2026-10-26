#!/usr/bin/env python3
"""Offline test: spins a local page (good and broken) and verifies LandingVerify catches both."""
import subprocess, sys, time, threading, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from landing_verify import verify


def make_server(good: bool):
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            if good and self.path == "/":
                self.send_response(200); self.end_headers()
                self.wfile.write(b"<html><body><h1>Real product page.</h1>"
                                 b"<p>Working content that readers can actually see and use every day.</p></body></html>")
            else:
                self.send_response(404); self.end_headers()
        def log_message(self, *a): pass
    s = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, f"http://127.0.0.1:{s.server_address[1]}/"


ok_srv, ok_url = make_server(True)
bad_srv, bad_url = make_server(False)
try:
    r1 = verify(ok_url, expect="Real product page")
    assert r1["http_status"] == 200 and r1["has_real_content"], "good page must pass basics"
    assert r1.get("expect_found"), "expected text must be found"
    r2 = verify(bad_url)
    assert r2["http_status"] == 404 and not r2["ok"], "broken page must fail: readers see nothing"
    print("ALL LANDING-VERIFY TESTS PASSED")
    print(json.dumps(r2, ensure_ascii=False)[:200])
finally:
    ok_srv.shutdown(); bad_srv.shutdown()
