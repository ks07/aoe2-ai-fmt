.PHONY: test clean

INPUTDIR = examples
BUILDDIR = build
PKGDIR   = perparse

$(PKGDIR)/PERParser.py $(PKGDIR)/PERLexer.py $(PKGDIR)/PERListener.py : PER.g4
	antlr4 -Dlanguage=Python3 -o $(BUILDDIR) PER.g4
	mv $(BUILDDIR)/*.py $(PKGDIR)/

test : export CLASSPATH = /usr/share/java/stringtemplate4.jar:/usr/share/java/antlr4.jar:/usr/share/java/antlr4-runtime.jar:/usr/share/java/antlr3-runtime.jar/:/usr/share/java/treelayout.jar
test : $(INPUTDIR)/*
	antlr4 -o $(BUILDDIR) PER.g4
	javac $(BUILDDIR)/*.java
	cd $(BUILDDIR); \
	for f in $^; do \
		echo "\n" $${f} "\n"; \
		grun PER per ../$${f} -tokens; \
		grun PER per ../$${f} -tree; \
	done

clean :
	rm -f *.java *.class PERParser.py PERLexer.py PERListener.py *.interp *.tokens
