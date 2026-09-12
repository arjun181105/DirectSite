"""Preview production-equivalent slash redirects and real 404 responses."""
import http.server,json,pathlib,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]/'dist'
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def do_GET(self):
        url=urllib.parse.urlsplit(self.path);path=urllib.parse.unquote(url.path)
        mode=urllib.parse.parse_qs(url.query).get('__qa__',[None])[0]
        if mode in {'success','reject','network'}:
            target=(ROOT/path.lstrip('/')/'index.html').resolve()
            if target.is_relative_to(ROOT) and target.is_file():
                harness=(ROOT.parent/'tests/form-harness.js').read_text().replace('__MODE__',mode)
                body=target.read_text().replace('<head>','<head><script>'+harness+'</script>',1).encode()
                self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
        if path.rstrip('/')=='/website-design':
            self.send_response(301);self.send_header('Location','/web-design/'+('?' + url.query if url.query else ''));self.end_headers();return
        return super().do_GET()
    def end_headers(self):
        self.send_header('X-Robots-Tag','noindex');super().end_headers()
    def send_error(self,code,message=None,explain=None):
        if code==404:
            body=(ROOT/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        else:super().send_error(code,message,explain)
if __name__=='__main__':
    print('DirectSite preview: http://127.0.0.1:8765',flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
