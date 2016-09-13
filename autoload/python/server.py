import logging  
import logging.handlers  
import sys

f = open('/tmp/ScalaComplete.log', 'w+')
handler = logging.StreamHandler(f)
fmt = '%(asctime)s |%(filename)s:%(lineno)s |%(name)s :%(message)s'  
  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
  
logger = logging.getLogger('server')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) 

def getLogger():
    return logger

def setLoggerLevel(level):
    logger.setLoggerLevel(level)
    
import time
import BaseHTTPServer
import urlparse
import subprocess as sub
import threading

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.

printerPath = ""
jarPaths = []

#ret map will map from original file name to result string
retMap = {}
working = set([""])

class Worker(threading.Thread):
    def __init__(s,line,col,aliaLine, aliaCol,filename,orgname):
        threading.Thread.__init__(s)
        s.line = line
        s.col = col
        s.aliaLine = aliaLine
        s.aliaCol = aliaCol
        s.filename = filename
        s.oname = orgname
        s.classPath = []

    def run(s):
        if len(s.classPath) == 0 and len(jarPaths) != 0:
            for i in jarPaths:
                append(s.classPath, '--classpath %s' % i)

        cmd = ['scalac'] + s.classPath[:] +['-Xplugin:%s' % printerPath, '-P:printMember:%s:%s' %(s.line,s.col) , '-nowarn', s.filename]
        logger.debug(cmd)
        p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()
        ret = {}
        if errors != "":
            ret['code'] = 400
            ret['body'] = errors
        else:
            ret['code'] = 200
            ret['body'] = output
        global retMap
        retMap = {}
        key1 ="%s:%s:%s"%(s.oname, s.line, s.col)
        key2 ="%s:%s:%s"%(s.oname, s.aliaLine, s.aliaCol)
        retMap[key1] = ret
        retMap[key2] = ret


class CompilerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_POST(s):
        global printerPath
        global jarPaths
        contentLen = int(s.headers.getheader('content-length', 0))
        body = s.rfile.read(contentLen)
        bodyDict = eval(body)
        printerPath = bodyDict['printer']
        jarPaths = bodyDict['jars']
        s.send_response(200)
        s.wfile.write("done")

    def getRet(s,key1,key2):
        ret = {}
        if key1 in retMap:
            ret = retMap[key1]
            retMap[key2] = ret
        elif key2 in retMap:
            ret = retMap[key2]
            retMap[key1] = ret
        else:
            ret['code'] = 400
            ret['body'] = "error from server"
        s.send_response(ret['code'])
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write(ret['body'])

    def do_GET(s):
        """Respond to a GET request."""
        pret = urlparse.urlparse(s.path)
        q = urlparse.parse_qs(pret.query)

        line = q['line'][0]
        col = q['col'][0]
        completeLine = q['completeLine'][0]
        completeCol = q['completeCol'][0]
        filename = q['filename'][0]
        oname = q['oname'][0]

        global working
        key1 ="%s:%s:%s"%(oname, line, col)
        key2 ="%s:%s:%s"%(oname, completeLine, completeCol)

        
        if key1 in retMap or key2 in retMap:
            s.getRet(key1,key2)
        else:
            if key1 in working or key2 in working:
                while key1 not in retMap and key2 not in retMap:
                    time.sleep(0.01)
                s.getRet(key1,key2)
                working = set([])
                return
            working = set([key1,key2])
            newT = Worker(completeLine, completeCol,line,col,filename, oname)
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
        logger.debug("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logger.debug("Server Stop - %s:%s" % (HOST_NAME, PORT_NUMBER))
