JAVAC=javac
ANTLR=java -jar /usr/local/lib/antlr-4.7.1-complete.jar
ANTLR_DIR_PYTHON=./antlr_python
ANTLR_DIR_JAVA=./antlr_java

ANTLR_FLAGS=-visitor
ANTLR_FLAGS_PYTHON=$(ANTLR_FLAGS) -o $(ANTLR_DIR_PYTHON) -Dlanguage=Python3
ANTLR_FLAGS_JAVA=$(ANTLR_FLAGS) -o $(ANTLR_DIR_JAVA) -package antlr_java

TMP_DIR=./tmp

GRUN=java org.antlr.v4.runtime.misc.TestRig

GRAMMAR=ISSL.g4

.PHONY: clean all

all: clean grammar
	$(JAVAC) $(ANTLR_DIR_JAVA)/*.java


clean:
	rm -fv $(ANTLR_DIR_JAVA)/*.class
	rm -fv $(ANTLR_DIR_JAVA)/*.interp
	rm -fv $(ANTLR_DIR_JAVA)/*.tokens
	rm -fv $(ANTLR_DIR_JAVA)/*.java
	rm -fv $(ANTLR_DIR_PYTHON)/*.pyc
	rm -fv $(ANTLR_DIR_PYTHON)/*.interp
	rm -fv $(ANTLR_DIR_PYTHON)/*.tokens
	rm -fv $(ANTLR_DIR_PYTHON)/*.py




grammar:
	$(ANTLR) $(ANTLR_FLAGS_PYTHON) $(GRAMMAR)
	$(ANTLR) $(ANTLR_FLAGS_JAVA) $(GRAMMAR)


test: all
	cp $(ANTLR_DIR_JAVA)/* $(TMP_DIR)/
	cp $(GRAMMAR) $(TMP_DIR)/
	cd $(TMP_DIR)
	$(GRUN) ISSL specification -gui ../tests/jans_cpu.issl
