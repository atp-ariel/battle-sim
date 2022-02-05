from .ast import *


def obtain_statements(list_statements: List, statements: Statements):
    list_statements.append(statements.statement)
    if statements.statements is not None:
        obtain_statements(list_statements, statements.statements)
    return list_statements


def obtain_classes(list_classes: List, classes: Classes):
    list_classes.append(classes.class_def)
    if classes.classes is not None:
        obtain_classes(list_classes, classes.classes)
    return list_classes


def obtain_params(list_params: List, params: Params):
    list_params.append((params.name, params.type))
    if params.params is not None:
        obtain_params(list_params, params.params)
    return list_params


def obtain_elif(br: Branch, elif_def: ElifDef):
    br.ifs.append(If(elif_def.expression, elif_def.body))
    if elif_def.elif_def is not None:
        obtain_elif(br, elif_def.elif_def)
    elif elif_def.else_def is not None:
        br.else_body = elif_def.else_def.body


def obtain_expressions(list_expressions: List, expressions: Expressions):
    list_expressions.append(expressions.expression)
    if expressions.expressions is not None:
        obtain_expressions(list_expressions, expressions.expressions)
    return list_expressions


def obtain_functions(list_func: List, functions: Functions):
    list_func.append(functions.function)
    if functions.functions is not None:
        obtain_functions(list_func, functions.function)
    return list_func


def obtain_attributes(list_attr: List, attributes: Attributes):
    list_attr.append(attributes.attr_def)
    if attributes.attributes is not None:
        obtain_attributes(list_attr, attributes.attributes)
    return list_attr


def build_program(tokens: List[str], nodes: List):
    statements = nodes.pop()
    classes = nodes.pop()
    bs_file = BsFile(obtain_classes([], classes),
                     obtain_statements([], statements))
    nodes.append(bs_file)


def build_statements1(tokens: List[str], nodes: List):
    statements = nodes.pop()
    statement = nodes.pop()
    statements = Statements(statement, statements)
    nodes.append(statements)


def build_statements2(tokens: List[str], nodes: List):
    statement = nodes.pop()
    statements = Statements(statement, None)
    nodes.append(statements)


def build_breack(tokens: List[str], nodes: List):
    nodes.append(Break())


def build_continue(tokens: List[str], nodes: List):
    nodes.append(Continue())


def build_type(tokens: List[str], nodes: List):
    type = Type(tokens[len(tokens)-1])
    nodes.append(type)


def build_return_type(tokens: List[str], nodes: List):
    top = tokens[len(tokens)-1]
    if top == 'void':
        nodes.append(ReturnType(top))
    else:
        type = nodes.pop()
        nodes.append(ReturnType(type.type))


def build_params1(tokens: List[str], nodes: List):
    params = nodes.pop()
    type = nodes.pop()
    params = Params(type.type, tokens[len(tokens)-3], params)
    nodes.append(params)


def build_params2(tokens: List[str], nodes: List):
    type = nodes.pop()
    params = Params(type.type, tokens[len(tokens)-1], None)
    nodes.append(params)


def build_func_def1(tokens: List[str], nodes: List):
    name = tokens[len(tokens)-8]
    block = nodes.pop()
    params = obtain_params([], nodes.pop())
    arg_names = [t[0] for t in params]
    arg_types = [t[1] for t in params]
    return_type = nodes.pop()
    func_def = FuncDef(name, return_type.type, arg_names,
                       arg_types, obtain_statements([], block))
    nodes.append(func_def)


def build_func_def2(tokens: List[str], nodes: List):
    name = tokens[len(tokens)-7]
    block = nodes.pop()
    return_type = nodes.pop()
    func_def = FuncDef(name, return_type, [], [],
                       obtain_statements([], block))
    nodes.append(func_def)


def build_if_def1(tokens: List[str], nodes: List):

    elif_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, obtain_statements([], block))
    branch = Branch([if_def], None)

    obtain_elif(branch, elif_def)

    nodes.append(branch)


def build_if_def2(tokens: List[str], nodes: List):

    else_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, obtain_statements([], block))
    branch = Branch([if_def], else_def.body)

    nodes.append(branch)


def build_if_def3(tokens: List[str], nodes: List):
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, obtain_statements([], block))
    branch = Branch([if_def], None)

    nodes.append(branch)


def build_elif_def1(tokens: List[str], nodes: List):
    elif_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, obtain_statements(
        [], block), elif_def, None)

    nodes.append(elif_def)


def build_elif_def2(tokens: List[str], nodes: List):
    else_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, obtain_statements(
        [], block), None, else_def)

    nodes.append(elif_def)


def build_elif_def3(tokens: List[str], nodes: List):

    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, obtain_statements([], block), None, None)

    nodes.append(elif_def)


def build_else_def(tokens: List[str], nodes: List):

    block = nodes.pop()
    else_def = ElseDef(obtain_statements([], block))
    nodes.append(else_def)


def build_while_def(tokens: List[str], nodes: List):

    block = nodes.pop()
    expression = nodes.pop()

    while_def = WhileDef(expression, obtain_statements([], block))

    nodes.append(while_def)


def build_decl(tokens: List[str], nodes: List):
    expression = nodes.pop()
    type = nodes.pop()
    name = tokens[len(tokens)-3]

    assign = Decl(type.type, name, expression)

    nodes.append(assign)


def build_assign(tokens: List[str], nodes: List):
    expression = nodes.pop()
    name = tokens[len(tokens)-3]

    assign = Assign(name, expression)

    nodes.append(assign)


def build_return1(tokens: List[str], nodes: List):
    expression = nodes.pop()
    return_stm = Return(expression)
    nodes.append(return_stm)


def build_return2(tokens: List[str], nodes: List):
    return_stm = Return(None)
    nodes.append(return_stm)


def build_expressions1(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    expression = nodes.pop()
    expressions = Expressions(expression, expressions)
    nodes.append(expressions)


def build_expressions2(tokens: List[str], nodes: List):
    expression = nodes.pop()
    expressions = Expressions(expression, None)
    nodes.append(expressions)


def build_ternary_expression(tokens: List[str], nodes: List):
    right = nodes.pop()
    condition = nodes.pop()
    left = nodes.pop()

    ternexp = TernaryExpression(left, condition, right)

    nodes.append(ternexp)


def build_disjunction(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    binexp = BinaryExpression('or', left, right)

    nodes.append(binexp)


def build_conjuction(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    binexp = BinaryExpression('and', left, right)

    nodes.append(binexp)


def build_inversion(tokens: List[str], nodes: List):
    expr = nodes.pop()
    inversion = Inversion(expr)
    nodes.append(inversion)


def build_comparision(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    aritexp = AritmeticBinaryExpression(tokens[len(tokens)-2], left, right)

    nodes.append(aritexp)


def build_aritmetic_expression(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()
    op = tokens[len(tokens)-2]

    aritexp = AritmeticBinaryExpression(op, left, right)

    nodes.append(aritexp)


def build_primary1(tokens: List[str], nodes: List):
    exp = nodes.pop()
    name = tokens[len(tokens)-1]

    primary = Primary(exp, name, None)

    nodes.append(primary)


def build_primary2(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    exp = nodes.pop()

    primary = Primary(exp, None, obtain_expressions([], expressions))

    nodes.append(primary)


def build_primary3(tokens: List[str], nodes: List):
    exp = nodes.pop()

    primary = Primary(exp, None, [])

    nodes.append(primary)


def build_Variable(tokens: List[str], nodes: List):
    nodes.append(Variable(tokens[len(tokens)-1]))


def build_Bool(tokens: List[str], nodes: List):
    nodes.append(Bool(tokens[len(tokens)-1]))


def build_Number(tokens: List[str], nodes: List):
    nodes.append(Number(tokens[len(tokens)-1]))


def build_None(tokens: List[str], nodes: List):
    nodes.append(MyNone())


def build_list1(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    exp_list = MyList(obtain_expressions([], expressions))
    nodes.append(exp_list)


def build_list2(tokens: List[str], nodes: List):
    exp_list = MyList([])
    nodes.append(exp_list)


def build_functions1(tokens: List[str], nodes: List):
    functions = nodes.pop()
    func = nodes.pop()

    functions = Functions(func, functions)

    nodes.append(functions)


def build_functions2(tokens: List[str], nodes: List):
    func = nodes.pop()

    functions = Functions(func, None)

    nodes.append(functions)


def build_attr_def(tokens: List[str], nodes: List):
    exp = nodes.pop()
    type = nodes.pop()
    name = tokens[len(tokens)-3]

    attribute = AttrDef(name, type.type, exp)

    nodes.append(attribute)


def build_attributes1(tokens: List[str], nodes: List):
    attributes = nodes.pop()
    attr_def = nodes.pop()

    attributes = Attributes(attr_def, attributes)

    nodes.append(attributes)


def build_attributes2(tokens: List[str], nodes: List):
    attr_def = nodes.pop()

    attributes = Attributes(attr_def, None)

    nodes.append(attributes)


def build_constructor1(tokens: List[str], nodes: List):
    attributes = nodes.pop()
    params = obtain_params([], nodes.pop())
    arg_names = [t[0] for t in params]
    arg_types = [t[1] for t in params]

    constructor = Constructor(arg_names, arg_types,
                              obtain_attributes([], attributes))

    nodes.append(constructor)


def build_constructor2(tokens: List[str], nodes: List):
    attributes = nodes.pop()

    constructor = Constructor([], [], obtain_attributes([], attributes))

    nodes.append(constructor)


def build_constructor3(tokens: List[str], nodes: List):
    nodes.append(Constructor([], [], []))


def build_class_def1(tokens: List[str], nodes: List):
    functions = nodes.pop()
    constructor = nodes.pop()
    name = tokens[len(tokens)-9]
    parent_name = tokens[len(tokens)-7]

    class_def = ClassDef(name, parent_name, constructor.arg_names, constructor.arg_types,
                         constructor.attributes, obtain_functions([], functions))

    nodes.append(class_def)


def build_class_def2(tokens: List[str], nodes: List):
    constructor = nodes.pop()
    name = tokens[len(tokens)-8]
    parent_name = tokens[len(tokens)-6]

    class_def = ClassDef(name, parent_name, constructor.arg_names,
                         constructor.arg_types, constructor.attributes, [])

    nodes.append(class_def)


def build_classes1(tokens: List[str], nodes: List):
    classes = nodes.pop()
    class_def = nodes.pop()
    classes = Classes(class_def, classes)
    nodes.append(classes)


def build_classes2(tokens: List[str], nodes: List):
    class_def = nodes.pop()
    classes = Classes(class_def, None)
    nodes.append(classes)
