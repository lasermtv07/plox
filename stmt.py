class Visitor():
    def visitExpression():
        pass
    def visitPrint():
        pass

class Expr():
    def __init__(self):
        pass

class Expression(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression

class Print(Expr):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression
