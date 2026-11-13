class Visitor():
    def visitExpression():
        pass
    def visitPrint():
        pass
    def visitVar():
        pass

class Expr():
    def __init__(self):
        pass

class Expression(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression
    
    def accept(self,visitor):
        visitor.visitExpression(self.expression)

class Print(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression
    
    def accept(self,visitor):
        visitor.visitPrint(self.expression)

class Var(Expr):
    def __init__(self,name,initializer):
        self.name=name
        self.initializer=initializer
    
    def accept(self,visitor):
        visitor.visitVar(self.name,self.initializer)