#!/usr/bin/python3

class PastryVisitor:
    def visitCruller():
        pass
    def visitBeignet():
        pass


class Pastry:
    def accept(self,visitor):
        pass

class Beignet(Pastry):
    def accept(self,visitor):
        visitor.visitBeignet()

class Cruller(Pastry):
    def accept(self,visitor):
        visitor.visitCruller()

class Bake(PastryVisitor):
    def visitCruller():
        print("Baking Cruller")
    def visitBeignet():
        print("Baking Beignet")

class Sell(PastryVisitor):
    def visitCruller():
        print("Sold Cruller for USD69")
    def visitBeignet():
        print("Sold Beignet for USD420")

beignet=Beignet()
cruller=Cruller()

beignet.accept(Bake)
cruller.accept(Sell)