.PHONY: gtest test clean lint dist

SHELL := /bin/bash

INPUTDIR = examples
BUILDDIR = build
PKGDIR   = performat/perparse
DISTDIR  = dist

PARSER_FILES = $(PKGDIR)/PERParser.py $(PKGDIR)/PERLexer.py $(PKGDIR)/PERListener.py

$(PARSER_FILES) : PER.g4
	antlr4 -Dlanguage=Python3 -o $(BUILDDIR) PER.g4
	mv $(BUILDDIR)/*.py $(PKGDIR)/

test : $(PARSER_FILES)
	TMP=$$(mktemp); \
	for f in ${INPUTDIR}/*.input.per; do \
		echo; echo "------------"; echo $${f}; echo "------------"; echo; \
		./format.py "$${f}" "$${TMP}"; \
		diff -q "$${TMP}" "$${f%.input.per}.tidy.per" || diff -y "$${TMP}" "$${f%.input.per}.tidy.per"; \
	done; \
	rm $${TMP}

gtest : export CLASSPATH = /usr/share/java/stringtemplate4.jar:/usr/share/java/antlr4.jar:/usr/share/java/antlr4-runtime.jar:/usr/share/java/antlr3-runtime.jar/:/usr/share/java/treelayout.jar
gtest : $(INPUTDIR)/*.input.per
	antlr4 -o $(BUILDDIR) PER.g4
	javac $(BUILDDIR)/*.java
	cd $(BUILDDIR); \
	for f in $^; do \
		echo "\n" $${f} "\n"; \
		grun PER per ../$${f} -tokens; \
		grun PER per ../$${f} -tree; \
	done

lint : $(PARSER_FILES)
	pylint performat

dist :
	python setup.py sdist bdist_wheel

clean :
	rm -rf $(BUILDDIR)/* $(PARSER_FILES) $(DISTDIR)/
