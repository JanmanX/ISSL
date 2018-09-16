JAVAC=javac
ANTLR=java -jar /usr/local/lib/antlr-4.7.1-complete.jar
ANTLR_DIR=./antlr
ANTLR_FLAGS=-o $(ANTLR_DIR)
GRUN=java org.antlr.v4.runtime.misc.TestRig

GRAMMAR=SMEDSL.g4

.PHONY: clean all

all: clean grammar
	$(JAVAC) $(ANTLR_DIR)/*.java

clean:
	rm -fv $(ANTLR_DIR)/*.class
	rm -fv $(ANTLR_DIR)/*.interp
	rm -fv $(ANTLR_DIR)/*.tokens

grammar: 
	$(ANTLR) $(ANTLR_FLAGS) $(GRAMMAR)


test: all
	$(GRUN) ./antlr/SMEDSL specification -gui example_dsl
