"""เปิดเว็บในเครื่องที่เส้นทางเดียวกับเว็บจริง"""
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit
from seo_config import ROOT, BASE_PATH
sys.stdout.reconfigure(encoding='utf-8')
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'site'),**kwargs)
    def do_GET(self):
        path=urlsplit(self.path).path
        if BASE_PATH and path==BASE_PATH:
            self.send_response(301);self.send_header('Location',BASE_PATH+'/');self.end_headers();return
        if BASE_PATH and not path.startswith(BASE_PATH+'/'):
            self.send_error(404);return
        self.path=self.path[len(BASE_PATH):] if BASE_PATH else self.path
        super().do_GET()
if __name__=='__main__':
    port=int(sys.argv[1]) if len(sys.argv)>1 else 8091
    print(f'เปิด http://127.0.0.1:{port}{BASE_PATH}/',flush=True)
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
