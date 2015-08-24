#!/bin/bash
shopt -s nocasematch

[ "${#@}" -eq "0" ] && echo "specify document files!" && exit 

for doc; do
    if [ "$(file $doc | tr -s \s | cut -d' ' -f2)" = "LaTeX" ]; then
        [ ${doc##*.} = "tex" ] && doc=${doc%.tex}
        latexmk -c ${doc}.tex
        rm -rf ${doc}.synctex.*
    else
        [ ! -e $doc ] && echo "$doc does not exist!" || echo "$doc is not a LaTeX document!"
    fi
done
