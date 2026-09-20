from expr import *

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.current=0
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        pass