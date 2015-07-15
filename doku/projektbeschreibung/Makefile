#


.PHONY: clean, all

all: Documentation.pdf

Documentation.pdf: Documentation.tex
	latexmk -xelatex -interaction=nonstopmode -synctex=1 $<

clean:
	latexmk -c Documentation.tex

purge: clean
	latexmk -C Documentation.tex

