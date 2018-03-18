import os, sys, re, time, http.server, socketserver
from socketserver import ThreadingMixIn

def splittext(tx):
    return re.findall('.', tx)

def separate(tx):
    foo = tx.split(" ")
    return ["<div>" + j + "</div>" for j in foo]

def separate2(tx):
    foo = tx.split(" ")
    return [j + " " for j in foo]

files = {
    '/': ["<!DOCTYPE html>"+
"""<html>\r
    <head>\r
    <title>Super slow web server!!</title>\r
    <style>body { font-family: helvetica, arial; font-weight: bold; }
        .column { float: left; width: 20%; margin-left: 20%; line-height: 100%; }
        .header { clear: left; font-weight: bold; font-size: 200%; }</style>
    </head>\r
    <body>\r\n"""] +
        ["<div class='header'>"] +
        splittext("What if...") +
        ["</div><div class='column'>"] +
        separate("one party controlled two branches of government and you wanted to protest them but") +
        ["</div><div class='column'>"] +
        separate("the page you were using to organize it loaded one word at a time") +
        ["</div>"] +
        ["<div class='header'>"] +
        splittext("and also...") +
        ["</div><div style='margin-left: 20%; line-height: 100%;'>"] +
        ["some ", "quote-", "unquote ", "tech ", "person ", "was ",
         "giving ", "you ", "technical ", "misinformation ",
        "about ", "how ", "browsers ", "deal ", "with ", "HTML?"] +
        ["</div>"] +
        ["</body></html>\r\n"]
}

lengths = {}

for f in files:
    lengths[f] = sum([len(j) for j in files[f]])

VERSION = "artificially slow server 0.1"

file_not_found_message = \
"""<!doctype html><html><head><title>File not found</title></head>
<body><p>You're enjoying <i>""" + VERSION + """</i>. Your file was not found. Fantastic!</p>
</body></html>"""

file_not_found_length = len(file_not_found_message)

HEADER = \
"""HTTP/1.1 %(response)s\r
Server: """+VERSION+"""\r
Content-Type: text/html; charset=utf-8\r
Content-Length: %(length)d
Cache-Control: no-cache\r
Connection: close\r\n\r\n"""

responses = {}
responseid = 0

def run():
        server_address = ('', 8080)
        httpd = ThreadedServer(server_address, SlowHandler)
        httpd.serve_forever()

class ThreadedServer (ThreadingMixIn, http.server.HTTPServer):
    "whee"

class SlowHandler (http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("asked for %s" % self.path)
        sys.stdout.flush()
        self.happy_response("/")
    def happy_response(self, path):
        self.response("200 OK", files[path], lengths[path])
    def not_found(self, path):
        self.response("404 Not Found",
            [file_not_found_message],
            file_not_found_length)
    def response(self, text, file, length):
        header = HEADER % {'response': text,
            'length': length}
        self.write(header)
        for i in range(len(file)):
            self.writeout(file[i])
            if i < len(file)-1:
                time.sleep(0.3)
        #chunk:
        #self.writeout("")
    def write(self, text):
        self.wfile.write(str.encode(text))
        self.wfile.flush()
    def writeout(self, text):
        wfile = self.wfile
        wfile.write(str.encode(text))
        #wfile.write(str.encode("%x\r\n"%len(text) + text + "\r\n"))
        wfile.flush()


if __name__ == '__main__':
    run()
