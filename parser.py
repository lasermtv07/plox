from expr import *
from lexer import TokenType,Token
import error as err

class ParseError:
    def __init__(self):
        pass

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.current=0
    
    #utility functions
    def isAtEnd(self):
        return self.peek().type==-1

    def peek(self) ->Token:
        return self.tokens[self.current]
    
    def previous(self) ->Token:
        return self.tokens[self.current-1]

    def check(self,type):
        if self.isAtEnd(): return False
        return self.peek().type==type

    def advance(self) ->Token:
        if not self.isAtEnd(): self.current+=1
        return self.previous()

    def match(self,*args:TokenType):
        for i in args:
            if self.check(i):
                self.advance()
                return True
        return False

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr=self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator=self.previous()
            right=self.comparison()
            expr=Binary(expr,operator,right)
        
        return expr

    def comparison(self):
        expr=self.term()

        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL):
            operator=self.previous()
            right=self.term()
            expr=Binary(expr,operator,right)

        return expr         

    def term(self):
        expr=self.factor()

        while self.match(TokenType.STAR,TokenType.SLASH):
            operator=self.previous()
            right=self.factor()
            expr=Binary(expr,operator,right)
        
        return expr

    def factor(self):
        expr=self.unary()

        while self.match(TokenType.PLUS,TokenType.MINUS):
            operator=self.previous()
            right=self.unary()
            expr=Binary(expr,operator,right)
        
        return expr

    def unary(self):
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator=self.previous()
            expr=Unary(operator,self.unary())
        else:
            expr=self.primary()
        
        return expr
    
    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER,TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr=self.expression()
            self.consume(TokenType.RIGHT_PAREN,"Expect ')' after expression")
            return Grouping(expr)

    def error(self,token:Token,message):
        err.error(token,message)
        return ParseError()

    def consume(self,type:TokenType,message):
        if self.check(type): return self.advance()
        
        self.error(self.peek(),message)

        # TODO:finish