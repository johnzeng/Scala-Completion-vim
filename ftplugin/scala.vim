func! ScalaComplete(findstart, base)
  return scala#complete(a:findstart,a:base)
endfunc

setlocal omnifunc=ScalaComplete
