import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from http.client import HTTPConnection
from neuroweave.server import make_server


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=make_server(0);cls.port=cls.server.server_port
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,method,path,body=None,headers=None):
        c=HTTPConnection('127.0.0.1',self.port,timeout=5)
        c.request(method,path,body=body,headers=headers or {});r=c.getresponse();status=r.status;head=dict(r.getheaders());data=r.read();c.close();return status,head,data
    def test_home(self):self.assertEqual(self.request('GET','/')[0],200)
    def test_api_chapters(self):self.assertEqual(len(json.loads(self.request('GET','/api/chapters')[2])),18)
    def test_health(self):self.assertEqual(self.request('GET','/api/health')[0],200)
    def test_live_run(self):
        r=self.request('POST','/api/run',json.dumps({'id':'chapter-10'}),{'Content-Type':'application/json'});self.assertEqual(r[0],200);self.assertTrue(json.loads(r[2])['result']['replay_equal'])
    def test_no_path_traversal(self):self.assertEqual(self.request('GET','/../../LICENSE')[0],404)
    def test_rebinding_host_rejected(self):self.assertEqual(self.request('GET','/',headers={'Host':'attacker.example'})[0],403)
    def test_cross_origin_rejected(self):self.assertEqual(self.request('POST','/api/run','{}',{'Content-Type':'application/json','Origin':'https://evil.example'})[0],403)
    def test_wrong_content_type(self):self.assertEqual(self.request('POST','/api/run','{}',{'Content-Type':'text/plain'})[0],415)
    def test_oversized_body(self):self.assertEqual(self.request('POST','/api/run','x'*16385,{'Content-Type':'application/json'})[0],413)
    def test_nonfinite_json(self):self.assertEqual(self.request('POST','/api/run','{"id":"chapter-10","seed":NaN}',{'Content-Type':'application/json'})[0],400)
    def test_unknown_field(self):self.assertEqual(self.request('POST','/api/run','{"id":"chapter-10","path":"/etc/passwd"}',{'Content-Type':'application/json'})[0],400)
    def test_unknown_lab(self):self.assertEqual(self.request('POST','/api/run','{"id":"other"}',{'Content-Type':'application/json'})[0],400)
    def test_security_headers(self):
        r=self.request('GET','/');self.assertEqual(r[1]['X-Content-Type-Options'],'nosniff');self.assertIn("frame-ancestors 'none'",r[1]['Content-Security-Policy'])


class CliTests(unittest.TestCase):
    def test_cli_list(self):
        r=subprocess.run([sys.executable,'-m','neuroweave','list'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0);self.assertEqual(len(r.stdout.strip().splitlines()),18)
    def test_cli_single(self):
        with tempfile.TemporaryDirectory() as d:
            r=subprocess.run([sys.executable,'-m','neuroweave','run','chapter-10','--out',d],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr);self.assertTrue((Path(d)/'index.html').exists())
    def test_cli_error(self):
        r=subprocess.run([sys.executable,'-m','neuroweave','run','no-such-lab'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
