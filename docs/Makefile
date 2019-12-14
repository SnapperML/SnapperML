PANDOC=/usr/local/bin/pandoc
RM=/bin/rm
METADATA_FILE=metadata.yaml
PANDOC_OPTIONS=--standalone --listings --metadata-file=$(METADATA_FILE)
PANDOC_PDF_OPTIONS=--filter pandoc-citeproc
PANDOC_LATEX_OPTIONS=-f markdown+smart -s -S --natbib

latex:
	$(PANDOC) *.md $(PANDOC_OPTIONS) $(PANDOC_LATEX_OPTIONS) -o thesis.tex

pdf:
	$(PANDOC) *.md $(PANDOC_OPTIONS) $(PANDOC_PDF_OPTIONS) -o thesis.pdf


.PHONY: all clean

all : pdf latex

clean:
	- rm -f thesis.pdf thesis.tex
