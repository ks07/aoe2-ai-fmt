.PHONY: test clean

INPUTDIR = examples

PERParser.py PERLexer.py PERListener.py : PER.g4
	antlr4 -Dlanguage=Python3 PER.g4

test : export CLASSPATH = /usr/share/java/stringtemplate4.jar:/usr/share/java/antlr4.jar:/usr/share/java/antlr4-runtime.jar:/usr/share/java/antlr3-runtime.jar/:/usr/share/java/treelayout.jar
test : $(INPUTDIR)/*
	antlr4 PER.g4 && javac *.java
	for f in $^; do \
		echo "\n" $${f} "\n"; \
		grun PER per $${f} -tokens; \
		grun PER per $${f} -tree; \
	done

clean :
	rm -f *.java *.class PERParser.py PERLexer.py PERListener.py *.interp *.tokens
