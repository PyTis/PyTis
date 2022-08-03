
set shiftwidth=2
set tabstop=2
set ts=2

source /home/jlee/.vim.php/syntax/php.vim
source /usr/share/vim/vim73/syntax/php.vim
source /home/jlee/.vim/plugins/taglist.vim
if getline(1) =~? '^\<\?php'
	set filetype=php
endif
