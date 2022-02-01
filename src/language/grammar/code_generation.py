from visitor import *
from my_ast import *
from io import StringIO

file=StringIO('')
count_tabs=0

class CodeGenerate:
    @visitor(BsFile)
    def visit(self, node : BsFile):
        
        count_tab+=1
        for class_def in node.classes:
            self.visit(class_def)
        
        count_tab-=1
        for statement in node.statements:
            self.visit(statement)    
        
        return str(file)

    @visitor(ClassDef)
    def visit(self, node : ClassDef):
        
        file.write(f'class {node.name}({node.parent}):\n')
        
        args=', '.join(arg.name for arg in node.attributes)
        
        
        if len(node.attributes) > 0:
            file.write(f'\tdef __init__({args})\n')
            
            for at in node.attributes:
                file.write(f'\t\t{at.name}={self.visit(at.init)}')
                
        for f in node.methods:
            args=', '.join( )
            file.write(f'\tdef {node.name}({args})\n')

    @visitor(Bear)
    def visit(self, animal):
        return "and bears, oh my!"
    
animals = [Lion(), Tiger(), Bear()]
visitor = ZooVisitor()
print(', '.join(visitor.visit(animal) for animal in animals))