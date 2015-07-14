#TEX=${wildcard *.tex}
#PDF=${TEX:.tex=.pdf}

.PHONY: clean

all: example-pres.pdf manual.pdf poster-beispiel.pdf GUI-use-case.png

example-pres.pdf manual.pdf poster-beispiel.pdf: example-pres.tex manual.tex poster-beispiel.tex
	latexmk -xelatex -interaction=nonstopmode -synctex=1 $<

GUI-use-case.pdf: GUI-use-case.tex
	latexmk -pdflatex=pdflatex -interaction=nonstopmode -synctex=1 $<

GUI-use-case.png: GUI-use-case.pdf
	gm convert -density 300 -type TrueColorMatte $< -trim $@

clean:
	latexmk -c *.tex
	-rm -f *.synctex*
	-rm -f GUI-use-case.png

purge: clean
	latexmk -C *.tex
