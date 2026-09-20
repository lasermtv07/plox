#!/usr/bin/python3

# TODO: Update for visitor
import sys


if len(sys.argv)<2:
    print("[error] enter  file name")
    sys.exit()

output='''
class Expr():
    def __init__(self):
        pass
'''



#generating subclasses
def genType(className,fields):
    global output

    output+=f"\nclass {className}(Expr):\n    def __init__(self,"

    for i in fields:
        output+=i+","

    output+="):\n        super().__init__()\n"

    for i in fields:
        output+=f"        self.{i}={i}\n"
    

inp=input(">> ")

while inp!="":
    head=inp.split(":")[0].strip()
    body=inp.split(":")[1].strip()

    bodyCopy=body.split(",")
    body=[]
    for i in bodyCopy:
        char=i.strip()

        #removes types
        for j in ["Expr","Object","Token"]:
            char=char.replace(j,"")
        
        char=char.strip()
        body.append(char)
    
    genType(head,body)
    inp=input(">> ")

with open(sys.argv[1],"w+") as f:
    f.write(output)
    f.close()