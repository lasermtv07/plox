# TODO: fix this weird shit
from lexer import TokenType
import error as err
class CastError(Exception):
    pass
class Visitor():
    def visitBinary():
        pass
    def visitGrouping():
        pass
    def visitLiteral():
        pass
    def visitUnary():
        pass
class RuntimeError(Exception):
    def __init__(self,message,token):
        self.message=message
        self.token=token
        super().__init__(self.message)

class Expr():
    def __init__(self):
        pass
    def accept(self):
        pass

class Binary(Expr):
    def __init__(self,left,operator,right):
        super().__init__()
        self.left=left
        self.operator=operator
        self.right=right
    
    def accept(self,visitor:Visitor):
        return visitor.visitBinary(self)


class Grouping(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression

    def accept(self,visitor:Visitor):
        return visitor.visitGrouping(self)

class Literal(Expr):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def accept(self,visitor:Visitor):
        return visitor.visitLiteral(self)

class Unary(Expr):
    def __init__(self,operator,right):
        super().__init__()
        self.operator=operator
        self.right=right

    def accept(self,visitor:Visitor):
        return visitor.visitUnary(self)

class AstPrinter(Visitor):
    def print(self,expr):
        return expr.accept(self)
    
    def parenthesize(self, *args):
        out="("
        for i in args:
            out+=" "
            if type(i)!=str:
            #    print(i,dir(i),i.accept(self),self)
                out+=i.accept(self)
            else:
                out+=i
        out+=")"
        return out
    
    def visitBinary(self,expr:Binary):
        return self.parenthesize(expr.operator.lexeme,expr.left,expr.right)

    def visitGrouping(self,expr:Grouping):
        return self.parenthesize("group ",expr.expression)
    
    def visitLiteral(self,expr:Literal):
        if expr.value==None: return "nil"
        return str(expr.value)

    def visitUnary(self,expr:Unary):
        return self.parenthesize(expr.operator.lexeme,expr.right)

class Interpreter(Visitor):
    def interpret(self,expr):
        try:
            value=self.evaluate(expr)
            return value
        except RuntimeError as e:
            err.error(e.token.line,e.message)
    def evaluate(self,expr):
        #print(expr.__dict__)
        return expr.accept(self)
    
    def checkNumberOperand(self,operator,left:Literal,right=None):
        if not (type(left)==int or type(left)==float):
            raise RuntimeError("Must be a number",operator)
        if not (type(right)==int or type(right)==float or right==None):
            raise RuntimeError("Must be a number",operator)

    def visitLiteral(self,expr:Literal):
        #print(expr.value)
        return expr.value
    
    def visitGrouping(self,expr:Grouping):
        return self.evaluate(expr.expression)
    
    def visitUnary(self,expr:Unary):
        right=self.evaluate(expr.right)
        if(expr.operator.type==TokenType.MINUS):
            self.checkNumberOperand(expr.operator,right,None)
            return -float(right)
        elif(expr.operator.type==TokenType.BANG):
            return not (False if not right or right==None else True)
        
    def visitBinary(self,expr:Binary):
        left=self.evaluate(expr.left)
        right=self.evaluate(expr.right)
        #print('OPERATOR', expr.operator.__dict__)
        match expr.operator.type:
            case TokenType.MINUS:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)-float(right)
            case TokenType.PLUS:
                #print('PLUS',left,right)
                if type(left)!=type(right):
                    raise RuntimeError("Types on both sides must match",expr.operator)
                if type(left)==float or type(left)==int:
                    return float(left)+float(right)
                elif type(left)==str:
                    return str(left)+str(right)
                else:
                    raise RuntimeError("Must be either an int or a string",expr.operator)

            case TokenType.SLASH:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)/float(right)
            case TokenType.STAR:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)*float(right)
            case TokenType.GREATER:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)>float(right)
            case TokenType.GREATER_EQUAL:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)>=float(right)
            case TokenType.LESS:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)<float(right)
            case TokenType.LESS_EQUAL:
                self.checkNumberOperand(expr.operator,left,right)
                return float(left)<=float(right)
            case TokenType.EQUAL_EQUAL: #be wary, for we doing some funky type casting here
                return left==right
            case TokenType.BANG_EQUAL:
                return left!=right
