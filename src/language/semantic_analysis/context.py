class Type:
    def __init__(self, context, name, parent=None):
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.parent = parent
        self.context = context

        if parent is not None:
            for m in parent.methods:
                self.methods[m] = parent.methods[m]

            for a in parent.attributes:
                self.attributes[a] = parent.attributes[a]

    def get_attribute(self, attribute):
        if attribute in self.attributes:
            return self.attributes[attribute]

    def get_method(self, method):
        if method in self.methods:
            return self.methods[method]

    def define_attribute(self, name, _type, attribute=None):
        self.attributes[name] = [attribute, _type]
        self.context.define_var(name, _type, attribute)
        # Se guarda en diccionario el atributo y el tipo

    def get_type(self, attribute):
        if attribute in self.attributes:
            _type = self.attributes[attribute]

            if _type == "func":
                _type = self.methods[attribute][0]

            return _type

        else:
            raise Exception(
                f"type object '{self.name}' has no attribute '{attribute}'")

    def define_method(self, name, return_type, arguments, argument_types):
        self.methods[name] = [return_type, arguments, argument_types]
        self.attributes[name] = [name, "func"]
        return self.context.define_func(name, return_type, arguments, argument_types)
        # Se guarda en diccionario el tipo de retorno, los argumentos y el tipo de los argumentos

    def is_attribute(self, name):
        return name in self.attributes

    def is_method(self, name):
        return name in self.methods


class Context:
    def __init__(self,name,father=None):
        self.name=name
        self.father = father
        self.children = {}
        self._var_context = {}
        self._func_context = {}
        self._type_context = {}
        # self._symbol_context={}

    def check_var(self, var):
        if self.father == None:
            return var in self._var_context

        else:
            if var in self._var_context:
                return True

            return self.father.check_var(var)

    def check_var_type(self, var, _type):
        if self.father == None:
            return var in self._var_context and self._var_context[var][0] == _type

        else:
            if var in self._var_context:
                return True

            return self.father.check_var(var)

    def check_func(self, func):
        if self.father == None:
            return func in self._func_context

        else:
            if func in self._func_context:
                return True

            return self.father.check_func(func)

    def check_func_args(self, func, args):
        if self.father == None:
            if func in self._func_context:
                if len(args) == len(self._func_context[func][1]):
                    for i in range(len(args)):
                        # print(self._func_context[func])
                        if args[i] != self._func_context[func][1][i]:
                            return False

                    return True

            return False

        else:
            if func in self._func_context:
                if len(args) == len(self._func_context[func][1]):
                    for i in range(len(args)):
                        if not args[i] != self._func_context[func][1][i]:
                            return False

                    return True

            return self.father.check_func_args(func, args)

    def get_type(self, var):
        if self.father is None:
            return self._var_context[var][0]

        else:
            return self.father.get_type(var)

    def define_var(self, var, _type, value=None):
        #print(self.is_type_defined(_type))
        if not var in self._var_context and self.is_type_defined(_type):
            self._var_context[var] = [_type, value]

        elif self._var_context[var][0] == _type:
            self._var_context[var][1] = value

        else:
            raise Exception("Type Error")

    def define_func(self, func, _type, args, _type_args):
        if self.is_type_defined(_type):

            if func in self._var_context:
                raise Exception(f"{func} is already defined")

            self._type_context[func] = ["function", None]

            data = [_type, [0]*len(args), [0]*len(args)]
            # [tipo de retorno,tipo de argumento,nombre de argumento]
            for i in range(len(args)):
                if self.is_type_defined(_type_args[i]):
                    data[2][i] = args[i]
                    data[1][i] = _type_args[i]

                    self._func_context[func] = data

                else:
                    raise Exception("Type Error")

        else:
            raise Exception("Type Error")

        return self.create_child_context(func)

    def create_child_context(self, name):
        child = Context(name,self)
        self.children[name] = child
        return child

    def create_type(self, name, parent=None):
        _parent = None
        if parent is not None:
            _parent = self.get_type_object(parent)
        child = self.create_child_context(name)
        t = Type(child, name, _parent)
        self._type_context[name] = t
        return [t,child]

    def get_return_type(self, func):

        if self.father is None:
            if self.check_func(func):
                return self._func_context[func][0]

            else:
                raise Exception("func '{func}' is not defined")

        else:
            if func in self._type_context:
                return self._func_context[func][0]

            else:
                return self.father.get_return_type(func)

    def get_type_object(self, name):
        if self.father is None:
            if name in self._type_context:
                return self._type_context[name]

            else:
                raise Exception("Type '{name}' is not defined")

        else:
            if name in self._type_context:
                return self._type_context[name]

            else:
                return self.father.get_type_object(name)

    def is_type_defined(self, name):
        if self.father is None:
            return name in self._type_context

        else:
            if name in self._type_context:
                return True

            else:
                return self.father.is_type_defined(name)
    
    def get_attr_type_children(self,name,_type):
        if len(self.children)==0:
            if name in self._var_context:
                _type=self._var_context[name][0]
                return

        for child in self.children:
            if name in self._var_context:
                _type=self._var_context[name][0]
                return

            self.children[child].get_attr_type_children(name,_type)

    # def define_symbol(symbol,type)
