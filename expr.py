# TODO: fix this weird shit
from lexer import TokenType
class Visitor():
    def visitBinary():
        pass
    def visitGrouping():
        pass
    def visitLiteral():
        pass
    def visitUnary():
        pass


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
    def evaluate(self,expr):
        #print(expr.__dict__)
        return expr.accept(self)
    
    def visitLiteral(self,expr:Literal):
        #print(expr.value)
        return expr.value
    
    def visitGrouping(self,expr:Grouping):
        return self.evaluate(expr.expression)
    
    def visitUnary(self,expr:Unary):
        right=self.evaluate(expr.right)
        if(expr.operator.type==TokenType.MINUS):
            return -float(right)
        elif(expr.operator.type==TokenType.BANG):
            return not (False if not right or right==None else True)
        
    def visitBinary(self,expr:Binary):
        left=self.evaluate(expr.left)
        right=self.evaluate(expr.right)
        #print('OPERATOR', expr.operator.__dict__)
        match expr.operator.type:
            case TokenType.MINUS:
                return float(left)-float(right)
            case TokenType.PLUS:
                #print('PLUS',left,right)
                if type(left)==float or type(left)==int:
                    return float(left)+float(right)
                if type(left)==str:
                    return str(left)+str(right)
            case TokenType.SLASH:
                return float(left)/float(right)
            case TokenType.STAR:
                return float(left)*float(right)
            case TokenType.GREATER:
                return float(left)>float(right)
            case TokenType.GREATER_EQUAL:
                return float(left)>=float(right)
            case TokenType.LESS:
                return float(left)<float(right)
            case TokenType.LESS_EQUAL:
                return float(left)<=float(right)
            case TokenType.EQUAL_EQUAL: #be wary, for we doing some funky type casting here
                return left==right
            case TokenType.BANG_EQUAL:
                return left!=right