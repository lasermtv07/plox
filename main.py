#!/usr/bin/python3
import sys
from lexer import TokenType,Token,Lexer
from error import error,report

hadError=False

def runFile(name):
    global hadError
    code=""
    with open(name,"r") as f:
        code=f.read()
        f.close()
    run(code)
    if hadError:
        sys.exit(65)
    

def runPrompt():
    while True:
        code=input(">> ")
        if code=="":
            continue
        run(code)


def run(code):
    print(code)

if __name__=="__main__":
    if len(sys.argv)>2:
        print("usage: main.py [script]")
    elif len(sys.argv)==2:
        runFile(sys.argv[1])
    else:
        runPrompt()