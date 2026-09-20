
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
        visitor.visitBinary()


class Grouping(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression

    def accept(self,visitor:Visitor):
        visitor.visitGrouping()

class Literal(Expr):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def accept(self,visitor:Visitor):
        visitor.visitLiteral()

class Unary(Expr):
    def __init__(self,operator,right):
        super().__init__()
        self.operator=operator
        self.right=right

    def accept(self,visitor:Visitor):
        visitor.visitUnary()

class AstPrinter(Visitor):
    def print(self,expr):
        return expr.accept(self)
    
    def visitBinary(self,expr:Binary):
        return "("+expr.operator.lexeme+" "+str(expr.left)+" "+str(expr.right)+")"

    def visitGrouping(self,expr:Grouping):
        return "(group "+str(expr.expression)+")"
    
    def visitLiteral(self,expr:Literal):
        return str(expr.value)

    def visitUnary(self,expr:Unary):
        return "("+expr.operator.lexeme+" "+str(expr.right)