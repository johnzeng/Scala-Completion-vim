func! scala#precompile()
    let a:line = line(".")
    let a:col = col(".")
    let a:buf = getline(a:line)
    exec 'normal %'
    let a:completeLine = line(".")
    let a:completeCol = col(".")
    let a:bufFile = s:saveCurrentBuffer(a:buf)
    execute 'pyfile '.g:clientPath
    let a:ret = cursor(a:line,a:col)
    return '.'
endfunc

func! scala#complete(findstart,base)
  if a:findstart
    let a:line = line(".")
    let a:col = col(".")
    let a:buf = getline(a:line)
    for i in range(a:col)
      "find dot
      if a:buf[a:col - i] == '.'
        let a:left = a:buf[0 : a:col -i-1]
        let a:right = a:buf[a:col :]
        let a:buf = a:left.a:right
        let a:completeCol = a:col - i + 1
        let a:completeLine = a:line
        break
      endif
    endfor
    let a:bufFile = s:saveCurrentBuffer(a:buf)
    execute 'pyfile '.g:clientPath
    let a:outList = split(a:out , '\n')
    if len(a:outList) < 2
      "this means gettting error
      echom a:out
      return -3
    endif
    if match(a:outList[0],'asldfkjaslfdlfd') == -1
      "this means gettting error
      echom a:out
      return -3
    endif
    for i in range(len(a:outList))
      if a:outList[i] == "Scope{"
        let a:start = i
      elseif a:outList[i] == "}"
        let a:end = i
        break
      endif
    endfor

    if !exists('a:start') || !exists('a:end') || a:start >= a:end - 1
      return -3
    endif

    let s:retList = a:outList[a:start + 1: a:end - 1]
    return a:completeCol
  else
    let a:retDicList = []
    for i in range(len(s:retList))
      let a:info = s:retList[i]
      if match(a:info, "\^\\s\*private") == 0 || match(a:info, "\^\\s\*protected") == 0
        continue
      endif

      let a:shortWord = substitute(a:info, "val ","", "")
      let a:shortWord = substitute(a:shortWord, "final ","","")
      let a:shortWord = substitute(a:shortWord, "package ","","")
      let a:shortWord = substitute(a:shortWord, "class ","","")
      let a:shortWord = substitute(a:shortWord, "object ","","")
      let a:shortWord = substitute(a:shortWord, "def ","","")
      let a:shortWord = substitute(a:shortWord, "extend ","","")
      let a:shortWord = substitute(a:shortWord, "override ","","")
      let a:shortWord = substitute(a:shortWord, "[ ;]","","g")

      let a:comWord = substitute(a:shortWord, "\[(:\].*","","")
      if a:comWord =~ '^'.a:base
        call add(a:retDicList,{'word':a:comWord, 'abbr':a:comWord, 'info':a:info})
      endif
    endfor
    return a:retDicList
  endif
endfunction

function! s:saveCurrentBuffer(lineBuf)
  let a:buf = getline(1, '$')
  let a:buf[line('.') - 1] = a:lineBuf
  if &encoding != 'utf-8'
    let a:buf = map(a:buf, 'iconv(v:val, &encoding, "utf-8")')
  endif
  if &l:fileformat == 'dos'
    " XXX: line2byte() depend on 'fileformat' option.
    " so if fileformat is 'dos', 'buf' must include '\r'.
    let a:buf = map(a:buf, 'v:val."\r"')
  endif
  let file = tempname()
  call writefile(a:buf, file)

  return file
endfunction
