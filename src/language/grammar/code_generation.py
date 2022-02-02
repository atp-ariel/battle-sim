from visitor import *
from my_ast import *
from io import StringIO

file=StringIO('')
count_tabs=0

def write(string):
    tab_string=''.join('\t' for i in range(count_tabs))
    file.write(tab_string+string)

class CodeGenerate:
    @visitor(BsFile)
    def visit(self, node : BsFile):
        
        for class_def in node.classes:
            self.visit(class_def)
        

        for statement in node.statements:
            self.visit(statement)    
        
        return str(file)

    @visitor(ClassDef)
    def visit(self, node : ClassDef):
        
        file.write(f'class {node.name}({node.parent}):\n')
        
        args=', '.join(arg.name for arg in node.attributes)        
        
        count_tabs+=1
         
        write(f'def __init__(self,{args}):\n')
            
        count_tabs+=1
        
        write(f'self.id=id\n')
        write(f'self.life_points = 5\n')
        write(f'self.defense = 3\n')
        write(f'self.map = None\n')
        write(f'self.cell : Cell = None\n')
        
        if node.parent=='LandUnit' or node.parent=='NavalUnit':
        
            write(f'self.side=None\n')
            write(f'self.moral = 5\n')
            write(f'self.attack = 6\n')
            write(f'self.solidarity = True\n')
            write(f'self.ofensive = 2\n')
            write(f'self.min_range = 1\n')
            write(f'self.max_range = 3\n')
            write(f'self.radio = 1\n')
            write(f'self.vision = 6\n')
            write(f'self.intelligence = 8\n')
            write(f'self.recharge_turns = 0\n')
            write(f'self.turns_recharging = 0\n')
            write(f'self.movil = True\n')
            write(f'self.intelligence = 8\n')
            write(f's self.no_defeated_units = 0\n')
            write(f'self.visited_cells = set()\n')
            
        for at in node.attributes:
            write(f'self.{at.name}={self.visit(at.init)}\n')
            
        count_tabs-=1
                
        for f in node.methods:
            self.visit(f)

    @visitor(FuncDef)
    def visit(self, node:FuncDef):
        
        args=', '.join(name for name in node.arg_names)
        file.write(f'def {node.name}({args}):\n')
        
        count_tabs+=1
        for statement in node.body:
            self.visit(statement)
    
    @visitor(Branch)
    def visit(self, node:Branch):
        
        initial=node.ifs[0]
        
        write(f'if {self.visit(initial.condition)}:\n')
        
        count_tabs+=1
        
        for statement in initial.body:
            self.visit(statement)
        
        count_tabs-=1
        
        total=len(node.ifs)
        
        if total>1:     
            for i in range(1,total):
                self.visit(node.ifs[i])
                
        if node.else_body is not None:
            count_tab+=1
            for statement in node.else_body:
                self.visit(statement)
            count_tab-=1
    
    @visitor(If)
    def visit(self, node:If):
        
        write(f'elif {self.visit(node.condition)}:\n')
        
        count_tabs+=1
        
        for statement in node.body:
            self.visit(statement)
            
        count_tabs-=1
    
    @visitor(WhileDef)    
    def visit(self,node: WhileDef):
        
        write(f'while {self.visit(node.condition)}:\n')
        
        count_tabs+=1
        
        for statement in node.body:
            self.visit(statement)
            
        count_tabs-=1
        
    @visitor(Decl)    
    def visit(self,node: Decl):
        write(f'{node.name}={self.visit(node.expression)}\n')
        
    @visitor(Assign)    
    def visit(self,node: Assign):
        write(f'{node.name}={self.visit(node.expression)}\n')
        
    @visitor(Return)
    def visit(self, node:Return):
        if node.expression is None:
            write('return\n')
        else:
            write(f'return {self.visit(node.expression)}')
        
    @visitor(Continue)
    def visit(self, node:Continue):
        write('continue\n')
        
    @visitor(Break)
    def visit(self, node:Break):
        write('break\n')
    
    @visitor(BinaryExpression)    
    def visit(self, node:BinaryExpression):
        
        left=self.visit(node.left)
        right=self.visit(node.right)
        
        return f'{left} {node.op} {right}'
    
    @visitor(TernaryExpression)
    def visit(self, node: TernaryExpression):
        
        left = self.visit(node.left)
        condition=self.visit(node.condition)
        right = self.visit(node.right)
        
        return f'{left} if {condition} else {rigth}'
    
    @visitor(Primary)
    def visit(self, node: Primary):
        
        exp=self.visit(node.expression)    
        if node.args is None:
            return f'{exp}.{node.name}\n'
        else:
            args=', '.join(self.visit(e) for e in node.args)
            
            return f'{exp}({args})\n'
    
    @visitor(Variable)        
    def visit(self, node: Variable):
        return node.name
    
    @visitor(Number)
    def visit(self, node: Number):
        return node.value
    
    @visitor(Bool)
    def visit(self,node:Bool):
        return node.value
    
    @visitor(MyNone)
    def visit(self,node:MyNone):
        return 'None'
    
    @visitor(MyList)
    def visit(self, node: MyList):
        args=', '.join(self.visit(e) for e in node.inner_list)
        return f'[{args}]'
    