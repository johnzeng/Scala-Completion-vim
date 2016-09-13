let s:pluginPath = expand('<sfile>:p')
let s:printerPathList = split(s:pluginPath, "/")[0:-2]
let s:printerPath = "/".join(s:jarPathList, '/')."/printer.jar"
"start the server from 
let s:serverState = system('python '.s:pluginPath.'/python/server.py&')
"set infercase

if !exists('g:scala_jar_list')
  let g:scala_jar_list = []
endif

func! SetupServer()
  let a:isSetup=1
  let a:pyfilePath = s:pluginPath.''
  pyfile ./autoload/python/client.py
endfunc

call SetupServer()

imap . <C-r>=scala#precompile()<CR>
func! ScalaComplete(findstart, base)
  return scala#complete(a:findstart,a:base)
endfunc

setlocal omnifunc=ScalaComplete
