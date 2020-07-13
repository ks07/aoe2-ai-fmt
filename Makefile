.PHONY: gtest test clean

SHELL := /bin/bash

INPUTDIR = examples
BUILDDIR = build
PKGDIR   = perparse

$(PKGDIR)/PERParser.py $(PKGDIR)/PERLexer.py $(PKGDIR)/PERListener.py : PER.g4
	antlr4 -Dlanguage=Python3 -o $(BUILDDIR) PER.g4
	mv $(BUILDDIR)/*.py $(PKGDIR)/

test : ${INPUTDIR}/*.input.per
	TMP=$$(mktemp); \
	for f in $^; do \
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

clean :
	rm -f $(BUILDDIR)/* $(PKGDIR)/PERParser.py $(PKGDIR)/PERLexer.py $(PKGDIR)/PERListener.py
