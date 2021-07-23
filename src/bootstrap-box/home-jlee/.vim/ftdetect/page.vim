set filetype=php
au BufRead,BufNewFile *.page            set filetype=php

if getline(1) =~? '^\<\?php'
	set filetype=php
endif
if exists("did_load_filetypes")
   finish
endif
augroup filetypedetect
   au! BufRead,BufNewFile *.page setfiletype php
augroup END 
