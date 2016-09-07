import time
import BaseHTTPServer
import urlparse
import subprocess as sub
import threading

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.

#ret map will map from original file name to result string
retMap = {}

class Worker(threading.Thread):
    def __init__(s,line,col,filename,orgname):
        threading.Thread.__init__(s)
        s.line = line
        s.col = col
        s.filename = filename
        s.oname = orgname

    def run(s):
        cmd = ['scalac', '-Xplugin:/Users/john/.vim/bundle/Scala-Completion-vim/printer.jar', '-P:printMember:%s:%s' %(s.line,s.col) , '-nowarn', s.filename]
        print cmd
        p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()
        ret = {}
        if errors != "":
            ret['code'] = 500
            ret['body'] = errors
        else:
            ret['code'] = 200
            ret['body'] = output
        global retMap
        retMap = {}
        retMap["%s:%s:%s"%(s.oname, s.line, s.col)] = ret


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

        line = q['line'][0]
        col = q['col'][0]
        filename = q['filename'][0]
        oname = q['oname'][0]

        print retMap
        key ="%s:%s:%s"%(oname, line, col) 
        if key in retMap:
            ret = retMap[key]
            s.send_response(ret['code'])
            s.send_header("Content-type", "text/plain")
            s.end_headers()
            s.wfile.write(ret['body'])
        else:
            newT = Worker(line,col,filename, oname)
            newT.start()
            s.send_response(200)
            s.send_header("Content-type", "text/plain")
            s.end_headers()
            s.wfile.write("")


if __name__ == '__main__':
    try:
        request = urllib2.urlopen("http://localhost:8000/ping")
        rsp = request.read()

    except :
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), CompilerHandler)
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
