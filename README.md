# Compiler for C Language

### CS335A Project 

* Source Language - C
* Intermediate Language - Python
* Assembly - x86/mips

### Milestone 1

## [Grammar link](http://www.quut.com/c/ANSI-C-grammar-y.html)
## How to run 
```sh
$ cd src
$ make 
$ cd ..
```
There are 5 code files name
* code1.c
* code2.c
* code3.c
* code4.c
* code5.c
```sh
$ ./bin/parser.sh ./test/code1.c
```
The parse tree is generated in the "test" folder.
```sh
$ cd test
```

After the execution go to the src directory and run.
```sh
$ make clean
```

### Members
* Kshitiz Suman 14333
* Rishabh Bhardwaj 14548

## Milestone 2
### How to run

Write the code in test folder of the Milestone 2 directory.Suppose that the code file name is code1.c. Then use
```sh
$ cd src
$ python parser.py ../test/code1.c 
```

* The output dump is generated in dump.txt in src folder.

* The symboltables are generated in the src folder with the names as their symboltablenumber.csv  . For ex: 1.csv 2.csv etc.


## Milestone 3 and Final Demo combined
### How to run

Write the code in the test folder of Milestone 4 directory.Suppose that the code file name in which you have written the c code is code1.c Then use
```sh
$ cd Milestone 4
$ cd src
$ python parser.py ../test/code1.c
```
* The 3 address code is generated in the file 3ac.txt
* The mips code of the C code is generated in the file code.asm
* For getting input from terminal use get(n) where n is any variable.
* For outputting the value of any variable in the terminal use put(n) .

 __**Salient Features**__

* We have used the register allocation scheme in which the labels get
register only if they are in use,i.e,they get freed as soon as they are not in use.This has been implemented by scanning the 3-ac from bottom as
taught in the class.
* If all the registers are busy and there is a demand, register is allotted on the basis of Least Recently Used Scheme.,i.e,the value is stored in the memory and that corresponding register is returned.
* The evaluation of any expression is optimum in this compiler.
* In case of arrays or to access memory, we have calculated the offset
value with the help of intermediate language (Python) ,if possible, to
reduce the use of registers.
* put() and get() functions have been implemented to output the value
and to get the value.
* typeof() function has been implemented which gives the type of any
expression passed as parameter.
* Constant folding feature has been implemented.

 __**Basic Features Implemented**__

* Native Data Types (Integer)
* Variables and Expressions
* Control Statements
  If else,|If |else if | else | ,If
  **Loops**  for , while
* Input / Output Statements
* Arrays
* Functions with Recursion feature


