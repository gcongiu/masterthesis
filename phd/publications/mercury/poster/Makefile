LATEXPARAM=
texmaster=poster

all: build 

build: 
	mkdir -p .tmp
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster}
	bibtex .tmp/${texmaster}
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster} # Second run for resolving references
	pdflatex -output-directory .tmp ${LATEXPARAM} ${texmaster} # Third run for getting everything in place
	mv .tmp/${texmaster}.pdf .

clean:
	rm -rf *.fls *.ps *.dvi *.log *.tmp *.out *.aux *.bbl *.blg *.toc *.lof *.lot *.synctex.gz *.fdb_latexmk *~
	rm -rf parts/*.aux
	rm -rf .tmp
	rm ${texmaster}.pdf
check:
	./textools/checkTex.sh parts/*.tex

count:
	detex parts/*.tex | wc -w
