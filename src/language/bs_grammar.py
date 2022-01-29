from .grammar import *

eof = Terminal("EOF")

bs_file = NonTerminal("bs_file")
statements = NonTerminal("statements")
statement = NonTerminal("statement")
simple_stmts = NonTerminal("simple_stmts")
complex_stmt = NonTerminal("complex_stmt")
simple_stat = NonTerminal("simple_stat")
NEWLINE = Terminal("NEWLINE", "\n")
func_def = NonTerminal("func_def")
if_def = NonTerminal("if_def")
class_def = NonTerminal("class_def")
while_def = NonTerminal("while_def")
assign = NonTerminal("assign")
return_stat = NonTerminal("return_stat")
_break = Terminal("break", value="break")
_continue = Terminal("continue", value="continue")
expressions = NonTerminal("expressions")
function = Terminal("function", "function")
name = Terminal("NAME")
lparent = Terminal("(", "(")
rparent = Terminal(")", ")")
arrow = Terminal("->", "->")
_if = Terminal("if", "if")
expression = NonTerminal("expression")
block = NonTerminal("block")
elif_def = NonTerminal("elif_def")
else_def = NonTerminal("else_def")
_elif = Terminal("elif", "elif")
_else = Terminal("else", "else")
_class = Terminal("class", "class")
_is = Terminal("is", "is")
_type = NonTerminal("type")
tnumber = Terminal("number", "number")
oeq = Terminal("=", "=")
_return = Terminal("return", "return")
lcurly = Terminal("{", "{")
rcurly = Terminal("}", "}")
params = NonTerminal("params")
comma = Terminal(",", ",")
disjunction = NonTerminal("disjunction")
_or = Terminal("or", 'or')
conjunction = NonTerminal("conjunction")
_and = Terminal("and", "and")
inversion = NonTerminal("inversion")
_not = Terminal("not", "not")
comparision = NonTerminal("comparision")
_sum = NonTerminal("sum")
compare_par = NonTerminal("compare_par")
_eq = Terminal("eq", "eq")
_neq = Terminal("neq", "neq")
_lte = Terminal("lte", "lte")
_lt = Terminal("lt", "lt")
_gte = Terminal("gte", "gte")
_gt = Terminal("gt", "gt")
plus = Terminal("+", "+")
term = NonTerminal("term")
minus = Terminal("-", "-")
factor = NonTerminal("factor")
mul = Terminal("*", "*")
div = Terminal("/", "/")
mod = Terminal("%", "%")
_pow = NonTerminal("pow")
opow = Terminal("^", "^")
primary = NonTerminal("primary")
dot = Terminal(".", ".")
atom = NonTerminal("atom")
args = NonTerminal("args")
_list = NonTerminal("list")
lbracket = Terminal("[", "[")
rbracket = Terminal("]", "]")
true = Terminal("True")
false = Terminal("False")
none = Terminal("None")
number = Terminal("NUMBER")
_while = Terminal("while", "while")
void = Terminal("void", "void")
return_type = NonTerminal("return_type")


bs_file += Production([statements, eof])
bs_file += Production([eof])

statements += Production([statement, statements])
statements += Production([statement])

statement += Production([simple_stmts])
statement += Production([complex_stmt])

simple_stmts += Production([simple_stat, NEWLINE, simple_stmts])
simple_stmts += Production([simple_stat])

complex_stmt += Production([func_def])
complex_stmt += Production([if_def])
complex_stmt += Production([class_def])
complex_stmt += Production([while_def])

simple_stat += Production([assign])
simple_stat += Production([return_stat])
simple_stat += Production([_break])
simple_stat += Production([_continue])
simple_stat += Production([expressions])

func_def += Production([function, _type, name, lparent, params, rparent, arrow, block], True)
func_def += Production([function, _type, name, lparent, rparent, arrow, block], True)

if_def += Production([_if, expression, arrow, block, elif_def], True)
if_def += Production([_if, expression, arrow, block, else_def], True)
if_def += Production([_if, expression, arrow, block], True)

elif_def += Production([_elif, expression, arrow, block, elif_def], True)
elif_def += Production([_elif, expression, arrow, block, else_def], True)
elif_def += Production([_elif, expression, arrow, block], True)

else_def += Production([_else, arrow, block], True)

class_def += Production([_class, name, _is, name, arrow, block], True)

while_def += Production([_while, expression, arrow, block], True)

return_type += Production([void])
return_type += Production([_type])

_type += Production([tnumber])
_type += Production([name])

assign += Production([_type, name, oeq, expression])

return_stat += Production([_return, expression])
return_stat += Production([_return])

block += Production([NEWLINE, lcurly, statements, rcurly])

params += Production([_type, name, comma, params])
params += Production([_type, name])

expressions += Production([expression, comma, expressions])
expressions += Production([expression])

expression += Production([disjunction, _if, disjunction, _else, expression])
expression += Production([disjunction])

disjunction += Production([conjunction, _or, disjunction])
disjunction += Production([conjunction])

conjunction += Production([inversion, _and, conjunction])
conjunction += Production([inversion])

inversion += Production([_not, inversion])
inversion += Production([comparision])

comparision += Production([_sum, compare_par])
comparision += Production([_sum])

compare_par += Production([_eq, _sum])
compare_par += Production([_neq, _sum])
compare_par += Production([_lte, _sum])
compare_par += Production([_lt, _sum])
compare_par += Production([_gte, _sum])
compare_par += Production([_gt, _sum])

_sum += Production([_sum, plus, term])
_sum += Production([_sum, minus, term])
_sum += Production([term])

term += Production([term, mul, factor])
term += Production([term, div, factor])
term += Production([term, mod, factor])
term += Production([factor])

factor += Production([plus, factor])
factor += Production([minus, factor])
factor += Production([_pow])

_pow += Production([primary, opow, factor])
_pow += Production([primary])

primary += Production([primary, dot, name])
primary += Production([primary, lparent, args, rparent])
primary += Production([primary, lparent, rparent])
primary += Production([atom])

args += Production([expression, comma, args])
args += Production([expression])

atom += Production([name])
atom += Production([true])
atom += Production([false])
atom += Production([none])
atom += Production([number])
atom += Production([_list])

_list += Production([lbracket, expressions, rbracket])
_list += Production([lbracket, rbracket])


GRAMMAR = Grammar(bs_file)
