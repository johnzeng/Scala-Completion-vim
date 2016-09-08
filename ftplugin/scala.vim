let s:pluginPath = expand('<sfile>:p')
let s:jarPathList = split(s:pluginPath, "/")[0:-2]
let s:jarPath = "/".join(s:jarPathList, '/')."/../printer.jar"
let s:serverState = system('python ./python/server.py&')
"set infercase

imap . <C-r>=scala#precompile()<CR>
func! ScalaComplete(findstart, base)
  return scala#complete(a:findstart,a:base)
endfunc

setlocal omnifunc=ScalaComplete
