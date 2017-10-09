#!/usr/bin/bash
var="$$1"
all: parser lexer

parser: parser.py
	python -m py_compile parser.py
	echo 'cd bin/;python parser.pyc ../$$1 > ../output.txt;clear; cd ..;cat output.txt' > parser.sh
	chmod 777 parser.sh
	mv *.pyc ../bin/
	mv *.sh ../bin/

lexer: lexer.py
	python -m py_compile lexer.py
	echo 'cd bin/;python lexer.pyc ../$$1; cd ..' > lexer.sh
	chmod 777 lexer.sh
	mv *.pyc ../bin/
	mv *.sh ../bin/

clean:
	rm -f ../*/*.pyc ../*/parsetab.py ../*/parser.out ../*/*.sh
