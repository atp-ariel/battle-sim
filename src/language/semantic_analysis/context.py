from ast import arg
from multiprocessing import context
from random import paretovariate


class Type:
    def __init__(self, context, name, def_context, parent=None):
        self.name = name
        self.parent = parent
        self.context = context
        self.def_context=def_context

        if parent is not None:
            parent_context=parent.context
            
            for v in parent_context._var_context:
                self.context._var_context[v]=parent_context._var_context[v]
                
                if parent_context._var_context[v][0]=="function":
                    self.context._var_context[v][1]=0
                                   
            for f in parent_context._func_context:
                self.context._func_context[f]=parent_context._func_context[f]
                
            for t in parent_context._type_context:
                self.context._type_context[t]=parent_context._type_context[t]

    def define_attribute(self, name, _type, attribute=None):
        if name in self.parent.context._var_context:
            if not self.context.check_var_type(name, _type):
                raise TypeError('The types did not match')
        else:
            self.context.define_var(name, _type, attribute)
        # Se guarda en diccionario el atributo y el tipo
        
    def define_method(self, name, return_type, arguments, argument_types):
        return self.context.define_func(name, return_type, arguments, argument_types)
        # Se guarda en diccionario el tipo de retorno, los argumentos y el tipo de los argumentos

    def is_attribute(self, name):
        return  self.context.check_var(name)

    def is_method(self, name):
        return self.context.check_func(name)
        
    def check_method(self, func, args):
        return self.context.check_func_args(func, args)
        
    def is_child(self,type_parent):
        if self.parent is None:
            return False
        
        if self.parent.name==type_parent.name:
            return True
        
        return self.parent.is_child(type_parent)
        

class Context:
    def __init__(self,name,father=None):
        self.name=name
        self.father = father
        self.children = {}
        self._var_context = {}
        self._func_context = {}
        self._type_context = {}
        self.If=0
        self.Else=0
        self.While=0
        # self._symbol_context={}

    def check_var(self, var):
        if self.father==None or self.is_type(self.father.name):
            return var in self._var_context

        else:
            if var in self._var_context:
                return  True
            
            else:
                return self.father.check_var(var)
 
    def check_var_type(self, var, _type):
        if self.check_var(var):
            type=self.get_type(var)
            
            if isinstance(type,list):
                type=type[1]
                
            if self.check_type(type,_type):
                return True
            
            else:
                return False
            
        else:
            raise Exception(f"{var} is not defined")

    def check_func(self, func):
        if self.father == None:
            return func in self._func_context

        else:
            if func in self._func_context:
                return True

            return self.father.check_func(func)

    def get_func(self,func):
        if self.father is None:
            return self._func_context[func]
        
        else:
            if func in self._func_context:
                return self._func_context[func]
            
            else:
                return self.father.get_func(func)
            
    def get_var(self,var):
        if self.father is None:
            return self._var_context[var]
        
        else:
            if var in self._var_context:
                return self._var_context[var]
            
            else:
                return self.father.get_var(var)
            
    def check_func_args(self, func, args):
        if self.check_func(func):
            _func=self.get_func(func)
          
            if len(args) == len(_func[1]):
                for i in range(len(args)):
                    if _func[1][i] != "Type" and not self.check_type(_func[1][i],args[i]):
                        return False

                return True
            
        else:
            return False

    def get_type(self, var):
        if self.check_var(var):
            return self.get_var(var)
        
        else:
            raise Exception(f"name {var} is not defined")


    def define_var(self, var, _type):
        
        type=_type
        if isinstance(_type,list):
            type=_type[1]
        
        if not self.check_var(var) and self.is_type_defined(type):
            self._var_context[var] = ["var", type]

        elif not self.is_type_defined(type):
            raise Exception(f"Type {type} is not defined")
        
        else:
            raise Exception(f"Var {var} is already defined")

    def define_func(self, func, _type, args, _type_args):
        if self.is_type_defined(_type) or _type == "void":

            if func in self._var_context:
                if self._var_context[func][0]=="function" and self._var_context[func][1]:
                    raise Exception(f"{func} is already defined")
                
                elif self._var_context[func][0]=="var":
                    raise Exception(f"Name {func} is the name for a variable")
                    
           
            self._var_context[func] = ["function",1, _type]
            _context=self.create_child_context(f"function {func}")
            data = [_type, [0]*len(args), [0]*len(args)]
            args_set=set()
            # [tipo de retorno,tipo de argumento,nombre de argumento]
            for i in range(len(args)):
                if self.is_type_defined(_type_args[i]):
                    if args[i] in args_set:
                        raise Exception(f"Some arguments have the same name in {func}")
                    args_set.add(args[i])
                    data[2][i] = args[i]
                    data[1][i] = _type_args[i]
                else:  
                    raise TypeError(f"The type {_type_args[i]} for the argument number {i} is not defined in function {func}")
                

        else:
            raise TypeError(f"The return type {_type.name} is not defined")
        
        self._func_context[func] = data
        for i in range(len(args)):
            _context.define_var(args[i],_type_args[i])
            
        return _context

    def create_child_context(self, name):
        child = Context(name,self)
        self.children[name] = child
        return child

    def create_type(self, name,args=[],type_args=[],parent=None,acces=True):
        _parent = None
        if parent is not None:
            _parent = self.get_type_object(parent)
            
            
        child = self.create_child_context(name)
        t = Type(child, name,self, _parent)
        self._type_context[name] = t
        
        context_func=None
        if acces:
            context_func=self.define_func(name,name,args,type_args)
            
        return [t,child,context_func]

    def get_return_type(self, func):
        if self.check_func(func):
            if self.father is None:
                return self._func_context[func][0]
   
            else:
                if func in self._func_context:
                    return self._func_context[func][0]

                else:
                    return self.father.get_return_type(func)
                
        else:
            raise Exception(f"func '{func}' is not defined")


    def get_type_object(self, name_type):
        name=name_type
        if isinstance(name,list):
            name=name_type[1]
        if self.father is None:
            if name in self._type_context:
                return self._type_context[name]

            else:
                raise Exception(f"Type '{name}' is not defined")

        else:
            if name in self._type_context:
                return self._type_context[name]

            else:
                return self.father.get_type_object(name)

    def is_type_defined(self, _name):
        name=_name
        if isinstance(name, list):
            name=name[1]
            
        if name=="None":
            return True
        
        if self.father is None:
            return name in self._type_context

        else:
            if name in self._type_context:
                return True

            else:
                return self.father.is_type_defined(name)
 
    def is_context_father(self,name):
        if self.father is None:
            return self.name==name
        
        else:
            if self.father.name==name:
                return True
            
            return self.father.is_context_father
              
    def get_context_father(self,name):
        if self.father is None and self.name==name:
            return self
        
        else:
            if self.father.name==name:
                return self.father
            
            return self.father.get_context_father
                      
    def is_in_while_context(self):
        if self.father is None:
            return self.Name(self.name,"While")
        
        else:
            if self.Name(self.father.name,"While"):
                return True
            
            return self.father.is_in_while_context()
        
    def is_in_func_context(self):
        if self.father is None:
            return self.Name(self.name,"function")
        
        else:
            if self.Name(self.name,"function"):
                return True
            
            return self.father.is_in_func_context()
        
    def check_type(self, type1,type2):
        #padre,hijo
        if self.is_type_defined(type1): 
            if type1==type2:
                return True
            
            if self.is_type_defined(type2):
                object1=self.get_type_object(type1)
                object2=self.get_type_object(type2)
                
                return object2.is_child(object1)
            
        return False
            
    def Name(self,name:str, type:str):
        temp=name.split(' ')
        
        if len(temp)<2:
            return False
        
        return temp[0] == type
        
    def is_type(self, name:str):
        if self.father is None:
            return name in self._type_context
        
        else:
            if name in self._type_context:
                return True
            
            else:
                return self.father.is_type(name)
    
        
    