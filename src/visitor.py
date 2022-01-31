import context

class Type_Collector:
    @visitor
    def visit(self,node:Program):
        self.context=Context()

        for classDef in node.classes:
            self.visit(classDef) #revisar esto

    @visitor
    def visit(self,node:ClassDef):
        self.context.create_type(node.name))

class Type_Builder:
    context:Context
    current_type:Type

    @visitor
    def visit(self,node:Program):
        for classDef in node.classes:
        self.visit(classDef)

    @visitor
    def visit(self,node:ClassDef):
        self.currentType=self.context.get_type(node.name)
        for attrDef in node.attributes:
            self.visit(attrDef)

        for methodDef in node.methods:
            self.visit(methodDef)

    @visitor
    def visit(self,node:AttrDef):
    attr_type=self.context.get_type(node.type)
    self.current_type.define_attribute(node.name,attr_type)

    @visitor
    def visit(self,node:MethodDef):
        return_type=self.context.get_type(node.return_type)
        arg_types=[self.context.get_type(t) for t in node.arg_types]
        self.current_type.define_method(node.name,return_type,node.arg_names,arg_types)

class Type_Checker:
    def __init__(self,context):
        self.context=context

    @visitor
    def visit(self,node:BinaryExpression,logger):
        self.visit(node.left,logger)
        self.visit(node.right,logger)

        if node.left.computed_type!=node.right.computed_type:
            logger.error("Type mismatch...")
            node.computed_type=None
            
        else:
            node.computed_type=node.left.computed_type

#Program cob node.Clases
#BinaryExpression node.computed_type
