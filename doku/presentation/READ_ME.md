Hinweise
========

Ich weis nicht mehr wer, aber jemand meinte bei WhatsApp,
dass es probleme gibt die geschichte mit tikz-uml zu installieren

ich habe meine non-standard `\*sty's` in dem dafür vorgesehenem Ordner:

~/texmf/tex/latex/local

    polemon ~/texmf/tex/latex/local % l
    tikz-uml.sty  timetable.sty

Alternativ, kann man die umgebunsvariable `TEXINPUTS` auf den ort
setzen, in dem sich die `.sty`-Dateien befinden. Dies jedoch versagt
fürchterlich bei `lualatex`.

*Ich empfehle immer `latexmk` zu benutzen. Bei dingen die indizes
erstellen müssen, kümmert sich `latexmk` um den mehrfachen aufruf.
Mit `latex -C` kann man problemlos temporäre dateien wieder entfernen.
