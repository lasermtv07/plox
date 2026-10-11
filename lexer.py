from enum import Enum
from error import error

class TokenType(Enum):
    #single char tokens
    LEFT_PAREN=1; RIGHT_PAREN=2; LEFT_BRACE=3; RIGHT_BRACE=4; COMMA=5; DOT=6; 
    MINUS=7; PLUS=8; SEMICOLON=9; SLASH=10; STAR=11

    #one or two character tokens
    BANG=12; BANG_EQUAL=13; EQUAL=14; EQUAL_EQUAL=15; GREATER=16; GREATER_EQUAL=17; 
    LESS=18; LESS_EQUAL=19

    #literals
    IDENTIFIER=20; STRING=21; NUMBER=22

    #keywords
    AND=23; CLASS=24; ELSE=25; FALSE=26; FUN=27; FOR=28; IF=29; NIL=30; OR=31; 
    PRINT=32; RETURN=33; SUPER=34; THIS=35; TRUE=37; VAR=38; WHILE=39; 

    EOF=40

keywords={
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":TokenType.SUPER,
    "this":TokenType.THIS,
    "true":TokenType.TRUE,
    "var":TokenType.VAR,
    "while":TokenType.WHILE
}

class Token:
    def __init__(self,type,lexeme,literal,line):
        self.type=type
        self.lexeme=lexeme
        self.literal=literal
        self.line=line

class Lexer:
    def __init__(self,source):
        self.source=source
        self.tokens=[]
        self.start=0
        self.current=0
        self.line=1

    def isAtTheEnd(self):
        return self.current>=len(self.source)
    
    def advance(self):
        ret=self.source[self.current]
        self.current+=1

        return ret

    def addToken(self,type,literal=None):
        text=self.source[self.start:self.current]
        self.tokens.append(Token(type,text,literal,self.line))

    def match(self,character):
        if self.isAtTheEnd():
            return False
        if self.source[self.current]!=character:
            return False
        self.current+=1
        return True

    def peek(self):
        if self.isAtTheEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current+1>=len(self.source):
            return '\0'
        return self.source[self.current+1]

    def string(self):
        while self.peek()!='\"' and not self.isAtTheEnd():
            if self.peek()=="\n":
                line+=1
            self.advance()
        if self.isAtTheEnd():
            error(self.line,"Unterminated string.")
            return
        
        self.advance()

        value=self.source[self.start+1:self.current-1] #TODO: fix start
        self.addToken(TokenType.STRING, value)
        return
    
    def isDigit(self,c):
        if c in ['0','1','2','3','4','5','6','7','8','9']:
            return True
        else:
            return False

    def isAlpha(self,c):
        return c=="_" or (ord(c)>=ord('A') and ord(c)<=ord('Z')) or (ord(c)>ord('A') and ord(c)<ord('Z'))

    def isAlphaNumeric(self,c):
        return self.isDigit(c) or self.isAlpha(c)

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek()=='.' and self.isDigit(self.peekNext()):
            self.advance()
        while self.isDigit(self.peek()):
            self.advance()       
        self.addToken(TokenType.NUMBER,float(self.source[self.start:self.current]))

    def identifier(self):
        global keywords
        while self.peek().isalnum():
            self.advance()
        
        #print(self.source[self.start:self.current])
        type=keywords.get(self.source[self.start:self.current].strip())
        if type==None:
            type=TokenType.IDENTIFIER

        self.addToken(type)

    def scanTokens(self):
        while not self.isAtTheEnd():
            self.start=self.current
            c=self.advance()

            match c:
                #single character tokens
                case '(': self.addToken(TokenType.LEFT_PAREN)
                case ')': self.addToken(TokenType.RIGHT_PAREN)
                case '{': self.addToken(TokenType.LEFT_BRACE)
                case '}': self.addToken(TokenType.RIGHT_BRACE)
                case ',': self.addToken(TokenType.COMMA)
                case '.': self.addToken(TokenType.DOT)
                case '-': self.addToken(TokenType.MINUS)
                case '+': self.addToken(TokenType.PLUS)
                case ';': self.addToken(TokenType.SEMICOLON)
                case '*': self.addToken(TokenType.STAR)

                #single or two character tokens
                case '!': 
                    self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
                case '=': 
                    self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
                case '<': 
                    self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
                case '>': 
                    self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

                #deleni, komentare
                case '/':
                    if self.match('/'):
                        while self.peek()!="\n" and not self.isAtTheEnd():
                            self.advance()
                    else:
                        self.addToken(TokenType.SLASH)
                
                #whitespaces
                case ' ':
                    pass
                case '\r':
                    pass
                case '\t':
                    pass
                case '\n':
                    self.line+=1
                
                #strings
                case '\"':
                    self.string()
                
                #numbers
                case _:
                    if c.isnumeric():
                        self.number()
                    elif c.isalnum():
                        self.identifier()
                    else:
                        print(c,ord(c))
                        error(self.line,"Unexpected character"); 
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return self.tokens

'''
with open("test.lox") as f:
    str=f.read()
    test=Lexer(str)
    f.close()
print(test.source)
test.scanTokens()
for i in test.tokens:
    print(i.type, i.lexeme, i.literal,type(i.literal))
'''