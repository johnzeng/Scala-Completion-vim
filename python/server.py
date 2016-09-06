import time
import BaseHTTPServer
import urlparse
import subprocess as sub

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.


class CompilerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_POST(s):
        pass

    def do_GET(s):
        """Respond to a GET request."""
        pret = urlparse.urlparse(s.path)
        q = urlparse.parse_qs(pret.query)

        p = sub.Popen(['scalac', '-Xplugin:/Users/john/.vim/bundle/Scala-Completion-vim/printer.jar', '-P:printMember:1:5' , '-nowarn','/Users/john/.vim/bundle/Scala-Completion-vim/test.scala'],stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()

        print output
        print errors
        
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write("hello")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), CompilerHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
