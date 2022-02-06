class Type:
    def __init__(self,name):
        self.name=name
        self.attributes={}
        self.methods={}

    def get_attribute(self,attribute):
        if attribute in self.attributes:
            return self.attributes[attribute]

    def get_method(self,method):
        if method in self.methods:
            return self.methods[method]
    
    def define_attribute(self,name,_type,attribute=None):
        self.attributes[name]=[attribute,_type]
        #Se guarda en diccionario el atributo y el tipo

        #Cómo me sé el tipo de attribute???????


    def define_method(self,name,return_type,arguments,argument_types):
        self.methods[name]=[return_type,arguments,argument_types]
        #Se guarda en diccionario el tipo de retorno, los argumentos y el tipo de los argumentos

    def is_attribute(self,name):
        return name in self.attributes

    def is_method(self,name):
        return name in self.methods

class Context:
    def __init__(self,father=None):
        self.father=father
        self.children=[]
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
        return self._var_context[var][0]

    def define_var(self,var,_type,value=None):
        if not var in self._var_context and _type in self._type_context:
            self._var_context[var]=[_type,value]

        elif self._var_context[var][0]==_type:
            self._var_context[var][1]=value

        else:
            raise Exception("Type Error")
   
    def define_func(self,func,_type,args,_type_args):
        if _type in self._type_context:
            
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

    def create_child_context(self):
        child=Context(self)
        self.children.append(child)
        return child
     
    def create_type(self,name):
        if name in self._type_context:
            return self._type_context[name]
            
        t=Type(name)
        self._type_context[name]=t
        return t

    def var_is_definied(self,name):
        return name in self._var_context

    def get_return_type(self,func):
        if self.check_func(func):
            return self._func_context[func][0]

    def get_type_object(self,name):
        if name in self._type_context:
            return self._type_context[name]
    #def define_symbol(symbol,type)
