
set filetype=sh
au BufRead,BufNewFile *.rc  set filetype=sh

if getline(1) =~? '^# \~\/.bashrc'
  set filetype=sh
endif
if exists("did_load_filetypes")
   finish
endif
augroup filetypedetect
   au! BufRead,BufNewFile *.rc setfiletype sh
augroup END
