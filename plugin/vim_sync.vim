python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! VSUpload()
python3 << endOfPython

from vim_sync import upload

upload()

endOfPython
endfunction


function! VSDownload()
python3 << endOfPython

from vim_sync import download

download()

endOfPython
endfunction


function! VSUploadFile()
python3 << endOfPython

from vim_sync import upload_file

upload_file()

endOfPython
endfunction


function! VSDownloadFile()
python3 << endOfPython

from vim_sync import download_file

download_file()

endOfPython
endfunction

command! VSUpload call VSUpload()
command! VSDownload call VSDownload()
command! VSUploadFile call VSUploadFile()
command! VSDownloadFile call VSDownloadFile()
