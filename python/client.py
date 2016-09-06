import urllib2
import urllib
import vim

params={
        "line":vim.eval('a:line'),
        "col":vim.eval('a:col'),
        "filename":vim.eval('a:bufFile'),
        "oname":"test",
        }
paramsStr = urllib.urlencode(params)
request = urllib2.urlopen("http://localhost:8000/?%s" % paramsStr)

rsp = request.read()

print rsp
vim.command("let a:out= '%s'" % rsp)
