class Type:
    def __init__(self,context,name,parent=None):
        self.name=name
        self.attributes={}
        self.methods={}
        self.parent=parent

        if not parent ins None:
            for m in parent.methods:
                self.methods[m]=parent.methods[m]

            for a in parent.attributes:
                self.attributes[a]=parent.attributes[a]

    def get_attribute(self,attribute):
        if attribute in self.attributes:
            return self.attributes[attribute]

    def get_method(self,method):
        if method in self.methods:
            return self.methods[method]
    
    def define_attribute(self,name,_type,attribute=None):
        self.attributes[name]=[attribute,_type]
        context.define_var(name,_type,attribute)
        #Se guarda en diccionario el atributo y el tipo

    def get_type(self,attribute):
        if attribute in self.attributes:
            _type=attributes[attribute]
        
            if _type=="func":
                _type=self.methods[attribute][0]

            return _type

        else:
            raise Exception(f"type object '{self.name}' has no attribute '{attribute}'")

    def define_method(self,name,return_type,arguments,argument_types):
        self.methods[name]=[return_type,arguments,argument_types]
        self.attributes[name]=[name,"func"]
        context.define_func(name,return_type,arguments,argument_types)
        #Se guarda en diccionario el tipo de retorno, los argumentos y el tipo de los argumentos

    def is_attribute(self,name):
        return name in self.attributes

    def is_method(self,name):
        return name in self.methods

class Context:
    def __init__(self,father=None):
        self.father=father
        self.children={}
        self._var_context={}
        self._func_context={}
        self._type_context={}
        #self._symbol_context={}

    def check_var(self,var):
        if self.father==None:
            return var in self._var_context

        else:
            if var in self._var_context:
                return True

            return self.father.check_var(var)

    def check_var_type(self,var,_type):
        if self.father==None:
            return var in self._var_context and self._var_context[var][0]==_type

        else:
            if var in self._var_context:
                return True

            return self.father.check_var(var)

    def check_func(self,func):
        if self.father==None:
            return func in self._func_context

        else:
            if func in self._func_context:
                return True

            return self.father.check_func(func)

    def check_func_args(self,func,args):
        if self.father==None:
            if func in self._func_context:
                if len(args)==len(self._func_context[func][1]):
                    for i in range(len(args)):
                        #print(self._func_context[func])
                        if  args[i]!=self._func_context[func][1][i]:
                            return False
                
                    return True

            return False

        else:
            if func in self._func_context:
                if len(args)==len(self._func_context[func][1]):
                    for i in range(len(args)):
                        if not args[i]!=self._func_context[func][1][i]:
                            return False
                
                    return True

            return self.father.check_func_args(func,args)

    def get_type(self,var):
        if self.father is None:
            return self._var_context[var][0]

        else:
            return father.get_type(var)

    def define_var(self,var,_type,value=None):
        if not var in self._var_context and _type in self._type_context:
            self._var_context[var]=[_type,value]

        elif self._var_context[var][0]==_type:
            self._var_context[var][1]=value

        else:
            raise Exception("Type Error")
   
    def define_func(self,func,_type,args,_type_args):
        if _type in self._type_context:
            self.create_child_context(func)
            
            if func in self._var_context:
                raise Exception(f"{func} is already defined")

            self._type_context[func]=["function",None]

            data=[_type,[0]*len(args),[0]*len(args)]
            #[tipo de retorno,tipo de argumento,nombre de argumento]
            for i in range(len(args)):
                if _type_args[i] in self._type_context:
                    data[2][i]=args[i]
                    data[1][i]=_type_args[i]
        
                    self._func_context[func]=data

                else:
                    raise Exception("Type Error")

        else:
            raise Exception("Type Error")

    def create_child_context(self,name):
        child=Context(self)
        self.children[name]=child
        return child
     
    def create_type(self,name,parent):     
        _parent=self.get_type_object(parent)       
        t=Type(name,_parent)
        self._type_context[name]=t
        child=self.create_child_context(name)
        return t

    def var_is_defined(self,name):
        return self.check_var(name)
        
    def get_return_type(self,func):
        
        if self.father is None:
            if self.check_func(func):
                return self._func_context[func][0]


            else:
                raise Exception("func '{func}' is not defined")

        else:
            if name in self._type_context:
                return self._func_context[func][0]

            else:
                return father.get_return_type(func)

    def get_type_object(self,name):
        if self.father is None:
            if name in self._type_context:
                return self._type_context[name]

            else:
                raise Exception("Type '{name}' is not defined")

        else:
            if name in self._type_context:
                return self._type_context[name]

            else:
                return father.get_type_object(name)

    def is_type_defined(self,name):
        if father is None:
            return name in self._type_context

        else:
            if name in self._type_context:
                return True

            else:
                return father.is_type_defined(name)
    #def define_symbol(symbol,type)
