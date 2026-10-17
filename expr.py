# TODO: fix this weird shit
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