from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *

class Type_Context:
    def __init__(self, context) -> None:
        self.context = context
        self.current_context=context
        self.ctor_context=None
        
    @visitor(BsFile)
    def visit(self, node: BsFile):
        for classDef in node.classes:
            self.visit(classDef)
            
        for statement in node.statements:
            self.visit(statement)
            self.current_context=self.context
            
    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        self.current_context=node.constructor_context
        for attrDef in node.attributes:    
            self.visit(attrDef)
            
        for methodDef in node.methods:
            self.current_context=node.my_context
            self.visit(methodDef)
        
        self.current_context=node.context
   
    @visitor(AttrDef)
    def visit(self, node: AttrDef):
        self.visit(node.init)
        
    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        if not self.current_context.check_func(node.name):
            node.context=self.current_context
            node.my_context=self.current_context.define_func(node.name, node.return_type, node.arg_names, node.arg_types)
        
        for s in node.body:
            self.current_context=node.my_context
            self.visit(s)
        
        self.current_context=node.context    
            
    @visitor(If)
    def visit(self,node:If):
        node.context=self.current_context
        node.my_context=node.context.create_child_context(f"If {node.context.If}")
        node.context.If+=1
        self.visit(node.condition)
        
        for s in node.body:
            self.current_context=node.my_context
            self.visit(s)
        
        self.current_context=node.context    
            
    @visitor(Branch)
    def visit(self,node:Branch):
        node.context=self.current_context
        
        for i in node.ifs:
            self.visit(i)
            
        self.current_context=node.context

        if not node.else_body is None:
            node.my_context=node.context.create_child_context(f"Else {node.context.Else}")
            
            for e in node.else_body:
                self.current_context=node.my_context
                self.visit(e)
                
            self.current_context=node.context
           
    @visitor(WhileDef)
    def visit(self,node:WhileDef):
        node.context=self.current_context
        node.my_context=node.context.create_child_context(f"While {node.context.While}")
        node.context.While+=1
        self.visit(node.condition)
        
        for s in node.body:
            self.current_context=node.my_context
            self.visit(s)
        
        self.current_context=node.context

    @visitor(Decl)
    def visit(self,node:Decl):
        node.context=self.current_context
        self.visit(node.expression)
        
    @visitor(Assign)
    def visit(self,node:Assign):
        node.context=self.current_context
        self.visit(node.expression)
        
    @visitor(Return)
    def visit(self,node:Return):
        node.context=self.current_context
        if node.expression is not None:
            self.visit(node.expression)
        
    @visitor(Break)
    def visit(self,node:Break):
        node.context=self.current_context
        
    @visitor(Continue)
    def visit(self,node:Continue):
        node.context=self.current_context
        
    @visitor(BinaryExpression)
    def visit(self,node:BinaryExpression):
        node.context=self.current_context
        self.visit(node.left)
        self.visit(node.right)  
        
    @visitor(AritmeticBinaryExpression)
    def visit(self,node:AritmeticBinaryExpression):
        node.context=self.current_context
        self.visit(node.left)
        self.visit(node.right)    
        
    @visitor(TernaryExpression)
    def visit(self,node:TernaryExpression):
        node.context=self.current_context
        self.visit(node.left)
        self.visit(node.condition)
        self.visit(node.right)
        
        
    @visitor(Inversion)
    def visit(self,node:Inversion):
        node.cortext=self.current_context
        self.visit(node.expression)
        
    @visitor(Primary)
    def visit(self,node:Primary):
        node.context=self.current_context
        
        self.visit(node.expression)
        self.current_context=node.context
        if not node.args is None:   
            for a in node.args:
                self.visit(a)
            
    @visitor(Variable)
    def visit(self,node:Variable):
        node.context=self.current_context 
                          
    @visitor(Number)
    def visit(self,node:Number):
        node.context=self.current_context
        
    @visitor(Bool)
    def visit(self,node:Bool):
        node.context=self.current_context
        
    @visitor(MyNone)
    def visit(self,node:MyNone):
        node.context=self.current_context
        
    @visitor(MyList)
    def visit(self,node:MyList):
        node.context=self.current_context   
            
    @visitor(PExpression)
    def visit(self,node:PExpression):
        node.context=self.current_context
        self.visit(node.expression)