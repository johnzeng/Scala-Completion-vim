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

try:
    request = urllib2.urlopen("http://localhost:8000/?%s" % paramsStr)
    rsp = request.read()
    vim.command("let a:out= '%s'" % rsp)
except urllib2.HTTPError, err:
    if err.code == 500:
        vim.command("let a:out = '%s'"% err.reason)

except urllib2.URLError, err:
    pass

