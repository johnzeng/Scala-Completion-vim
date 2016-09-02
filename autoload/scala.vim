func! scala#complete(findstart,base)
  if a:findstart
    let a:line = line(".")
    let a:col = col(".")
    let a:bufFile = s:saveCurrentBuffer(a:line,a:col)
    let a:out = system('scalac -Xplugin:printer.jar -P:printMember:'.a:line.':'.a:col.' -nowarn '.a:bufFile)
    let a:outList = split(a:out , '\n')
    let s:retList = a:outList[1:-2]
    return 1
  else
    let a:retDicList = []
    for i in range(len(s:retList))
      let a:info = s:retList[i]
      let a:word = matchstr(s:retList[i],"\.\*(" )
      let a:shortWord = substitute(a:word, "\.\*def ","","")
      let a:comWord = substitute(a:shortWord, "(","","")
      let a:retDicList += [{'word':a:comWord, 'abbr':a:info, 'info':a:info}]
    endfor
    echom a:retDicList[0]['word']
    return {'words': a:retDicList, 'refresh': 'always'}
  endif
endfun

function! s:saveCurrentBuffer(line,col)
  let buf = getline(1, '$')
  for i in range(a:col)
    "find dot
    if buf[a:line - 1][a:col - i] == '.'
      let left = buf[a:line - 1][0:a:col -i-1]
      let right = buf[a:line - 1][a:col:]
      let buf[a:line - 1] = left.right
      break
    endif
  endfor
  if &encoding != 'utf-8'
    let buf = map(buf, 'iconv(v:val, &encoding, "utf-8")')
  endif
  if &l:fileformat == 'dos'
    " XXX: line2byte() depend on 'fileformat' option.
    " so if fileformat is 'dos', 'buf' must include '\r'.
    let buf = map(buf, 'v:val."\r"')
  endif
  let file = tempname()
  call writefile(buf, file)

  return file
endfunction
