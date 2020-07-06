.PHONY: test clean

PERParser.py :
	antlr4 -Dlanguage=Python3 PER.g4

test : export CLASSPATH = /usr/share/java/stringtemplate4.jar:/usr/share/java/antlr4.jar:/usr/share/java/antlr4-runtime.jar:/usr/share/java/antlr3-runtime.jar/:/usr/share/java/treelayout.jar
test :
	antlr4 PER.g4 && javac *.java
	grun PER per testinput -tokens

clean :
	rm -f *.java *.class PERParser.py PERLexer.py PERListener.py *.interp *.tokens
