LATEXPARAM=
texmaster=main
texprint=print

all: ebook print

ebook:
	mkdir -p .tmp
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster}
	bibtex .tmp/${texmaster}
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster} # Second run for resolving references
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster} # Third run for getting everything in place
	mv .tmp/${texmaster}.pdf .

print:
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texprint}
	bibtex .tmp/${texprint}
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texprint} # Second run for resolving references
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texprint} # Third run for getting everything in place
	mv .tmp/${texprint}.pdf .

clean:
	rm -rf *.fls *.ps *.dvi *.log *.tmp *.out *.aux *.bbl *.blg *.toc *.lof *.lot *.synctex.gz *.fdb_latexmk *~
	rm -rf chapters/*.aux
	rm -rf .tmp
	rm *.pdf
check:
	./textools/checkTex.sh parts/*.tex

count:
	detex chapters/*.tex | wc -w
