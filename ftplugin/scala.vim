let s:pluginPath = expand('<sfile>:p')
let s:pluginPath = join(split(s:pluginPath, "/")[0:-3], '/')
let s:printerPath = "/".s:pluginPath."/autoload/printer.jar"
"start the server from 
let s:serverState = system('python /'.s:pluginPath.'/autoload/python/server.py&')
let g:clientPath = '/'.s:pluginPath."/autoload/python/client.py"
"set infercase

if !exists('g:scala_jar_list')
  let g:scala_jar_list = []
endif

func! SetupServer()
  let a:isSetup=1
  let a:pyfilePath = s:pluginPath.''
  exec 'pyfile '.g:clientPath
endfunc

call SetupServer()

imap . <C-r>=scala#precompile('.')<CR>
ino <Space> <Esc>
"imap <Space> <C-r>=scala#precompile(' ')<CR>
func! ScalaComplete(findstart, base)
  return scala#complete(a:findstart,a:base)
endfunc

setlocal omnifunc=ScalaComplete
