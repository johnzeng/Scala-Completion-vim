func! scala#complete(findstart,base)
  if a:findstart
    let a:line = line(".")
    let a:col = col(".")
    let buf = getline(a:line)
    let a:tocomplete = a:col
    for i in range(a:col)
      "find dot
      if buf[a:col - i] == '.'
        let left = buf[0:a:col -i-1]
        let right = buf[a:col:]
        let buf = left.right
        echom buf
        let a:tocomplete = a:col - i + 1
        break
      endif
    endfor
    let a:bufFile = s:saveCurrentBuffer(buf)
    let a:out = system('scalac -Xplugin:printer.jar -P:printMember:'.a:line.':'.a:col.' -nowarn '.a:bufFile)
    let a:outList = split(a:out , '\n')
    if len(a:outList) < 2
      return -1
    endif
    let s:retList = a:outList[1:-2]
    return a:tocomplete
  else
    let a:retDicList = []
    for i in range(len(s:retList))
      let a:info = s:retList[i]
      let a:shortWord = substitute(a:info, "\.\*def ","","")
      let a:comWord = substitute(a:shortWord, "\[(:\].*","","")
      echom 'word:'.a:comWord
      if a:comWord =~ '^'.a:base
        let a:retDicList += [{'word':a:comWord, 'abbr':a:comWord, 'info':a:info}]
      endif
    endfor
    echom a:retDicList[0]['word']
    return {'words': a:retDicList, 'refresh': 'always'}
  endif
endfun

function! s:saveCurrentBuffer(lineBuf)
  let buf = getline(1, '$')
  let buf[line('.') - 1] = a:lineBuf
  echom buf[line('.') -1]
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
