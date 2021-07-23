
cnoremap wq w

"autocmd Bufwritepre,filewritepre  * :set fileformat=unix
set ff=unix

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" for screen use
" opened in another screen? lets not play where's waldo anymore! 
" this will politely tell me which screen's window it is open in so that I may
" go close it if I want, but still provide me the normal options
"
augroup NoSimultaneousEdits
    autocmd!
		autocmd SwapExists * :call PrintScreenWindow() 
augroup END

function! PrintScreenWindow ()
  let fname = expand("%:p")
  " fix fname here, remove the path and leave only the filename/basename
  let fname =  fnamemodify(fname, ':t')
  " I just added the 'fpath', and 'all' variables,
  " The below my_command USED to use fname, but I found that if you have the
  " file open somewhere else (in a different screen window) AND also, have the
  " same filename, with a different path open, in a different window, it
  " causes an error, I.E.:
  " /root/abc/test.txt -- open in window 0
  " /root/abc/def/test.text -- open in window 1
  " now, in window 2, try to open /root/abc/test.txt, the below my_command
  " USED to have the variable 'fname', where it now has the variable 'all'
  " and this caused an error.
  " Adding this 'fpath', and 'all', fixes this issue.
  let fpath = expand("%:p:h")
  let all = fpath . "/." . fname
  " you might have to fix your path to lsof
  let my_command = "/usr/sbin/lsof | /bin/grep '" . all . ".swp' | /bin/grep " . $USER . " | sed -n 's/^vim\\? \\+\\([0-9]\\+\\).*$/\\1/p' "
  let result = substitute(system(my_command), '\n','','')
  if result
    let my_cmd2 = "cat /proc/" . result . "/environ | xargs -0 echo | sed -n 's/.*WINDOW=\\([0-9]*\\).*/\\1/p' "
    let res2 = substitute(system(my_cmd2), '\n','','')
    if res2 || res2 == '0'
      echo 'This file is already opened in window: ' . res2
    else
      echo "command failed: " . my_cmd2
    endif
  else
    echo my_command . " : cmd failed"
  endif
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


syntax on
filetype detect
filetype plugin on


"if did_filetype()       " filetype already set..
"	finish                " ..don't do these checks
"endif
"filetype plugin indent on
"syn on
" source /home/leejo7a/.vim.php/syntax/php.vim

"
"
hi Comment ctermbg=black ctermfg=darkgreen cterm=bold
syntax match Tab /\t/
hi Tab gui=underline guifg=blue ctermbg=blue 
source /home/leejo7a/.vim/syntax/tabcolor.vim

" Whitespace handling
"set expandtab
set shiftwidth=2
"set softtabstop=2   " VIM see multiple space characters as tabstops
set tabstop=2
"set ts=2
set autoindent      " automatically match the indent in the line below
set smartindent
set smartcase       " if there are no uppercase characters, we use insensitive
                    " search, else sensitive.


" General UI
set scrolloff=5     " Minimal number of screen lines to keep above and below
                    " the cursor.
set wmh=0           " Don't show anything but the status bar on minimized buffers
set matchpairs=(:),{:},[:],<:> " Matching pair characters
set showmatch       " show matching {,[,( when closing and opening set splitbelow      " open new window buffers below the current one instead of
                    " above
set ttyfast         " yes, we use a faster terminal
set shell=bash
set hls

" Completes the command if using the tab.
set wildmode=longest,list

" Turn off the aweful orange search color
hi Search ctermbg=LightGrey ctermfg=Black

" Customized Behavior
" make the file open prompt use the last directory that a file was opened in
" instead of curdir
" autocmd BufEnter * if bufname("") !~ "^\[A-Za-z0-9\]*://" | lcd %:p:h | endif


" Shortcuts
map <C-J> <C-W>j<C-W>_      " Easy browsing through multiple files
map <C-K> <C-W>k<C-W>_

"------------------------------------------------------------------------------
" Correct typos.
"------------------------------------------------------------------------------
" English.
iab beacuse    because
iab becuase    because
iab acn        can
iab cna        can
iab centre     center
iab chnage     change
iab chnages    changes
iab chnaged    changed
iab chnagelog  changelog
iab Chnage     Change
iab Chnages    Changes
iab ChnageLog  ChangeLog
iab debain     debian
iab Debain     Debian
iab defualt    default
iab Defualt    Default
iab differnt   different
iab diffrent   different
iab emial      email
iab Emial      Email
iab english    English
iab hebrew     Hebrew
iab currect    correct 
iab figth      fight
iab figther    fighter
iab fro        for
iab fucntion   function
iab ahve       have
iab homepgae   homepage
iab logifle    logfile
iab lokk       look
iab lokking    looking
iab mial       mail
iab Mial       Mail
iab miantainer maintainer
iab amke       make
iab mroe       more
iab nwe        new
iab recieve    receive
iab recieved   received
iab erturn     return
iab retrun     return
iab retunr     return
iab seperate   separate
iab shoudl     should
iab soem       some
iab taht       that
iab thta       that
iab teh        the
iab tehy       they
iab truely     truly
iab waht       what
iab wiht       with
iab whic       which
iab whihc      which
iab yuo        you
iab databse    database
iab versnio    version
iab obnsolete  obsolete
iab flase      false
iab recrusive  recursive
iab Recrusive  Recursive
iab destribution distribution

