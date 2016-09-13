import urllib2
import urllib
import vim

isSetup = vim.eval('exists("a:isSetup")')
if isSetup == '1':
    params={
            "printer":vim.eval('s:printerPath'),
            "jars":vim.eval('g:scala_jar_list')
            }
    try:
        request = urllib2.urlopen("http://localhost:8000/" ,data = str(params ))
        rsp = request.read()
        vim.command("let a:out= '%s'" % rsp)
    except urllib2.HTTPError, err:
        if err.code == 500:
            vim.command("let a:out = '%s'"% err.reason)

    except urllib2.URLError, err:
        pass

else:
    params={
            "completeLine":vim.eval('a:completeLine'),
            "completeCol":vim.eval('a:completeCol'),
            "line":vim.eval('a:line'),
            "col":vim.eval('a:col'),
            "filename":vim.eval('a:bufFile'),
            "oname":"test",
            }
    paramsStr = urllib.urlencode(params)

    try:
        vim.command("echom 'now open url'")
        request = urllib2.urlopen("http://localhost:8000/?%s" % paramsStr)
        vim.command("echom 'now read url'")
        rsp = request.read()
        vim.command("echom 'now rsp is:%s'" % rsp)
        vim.command("let a:out= '%s'" % rsp)
        vim.command("echom a:out")
    except urllib2.HTTPError, err:
        if err.code == 400:
            error_message = err.read()
            if "" != error_message:
                vim.command("let a:out = '%s'" % error_message.replace("'", ""))
            else:
                vim.command("let a:out='%s'" % err.reason)

    except urllib2.URLError, err:
        pass

