# Battle Script grammar

```
bs_file ->  statements EOF
        |   EOF

statements ->   statement statements
            |   statement

statement ->    simple_stmts
            |   complex_stmt

simple_stmts -> simple_stat NEWLINE simple_stmts
            |   simple_stats

complex_stmt -> func_def
            |   if_def
            |   class_def
            |   while_def

simple_stat ->  assign
            |   return_stat
            |   'break'
            |   'continue'
            |   expressions

func_def ->     'function' NAME '(' params ')' '->' block
            |   'function' NAME '(' ')' '->' block

if_def ->   'if' expression '->' block elif_def
        |   'if' expression '->' block else_def
        |   'if' expression '->' block

elif_def ->     'elif' expression '->' block elif_def
            |   'elif' expression '->' block else_def
            |   'elif' expression '->' block

else_def -> 'else' '->' block

class_def ->    'class' NAME 'is' NAME '->' block
            |   'class' NAME' '->' block

while_def ->    'while' expression '->' block

type ->     'number' 
        |   NAME

assign ->  type NAME '=' expression
        |  type NAME augassign expression

return_stmt ->  'return' expression
            |   'return'

block ->    NEWLINE INDENT statements DEDENT

params ->   type NAME ',' params
        |  type NAME

augassign ->    '+='
            |   '-='
            |   '*='
            |   '/='
            |   '%='

expressions ->  expression ','  expressions
            |   expression

expression ->   disjunction 'if' disjunction 'else' expression
            |   disjunction

disjunction ->  conjunction 'or' disjunction
            | conjunction

conjunction ->  inversion 'and' conjunction
            |   inversion

inversion ->    'not' inversion
            |    comparision


comparision ->  sum compare_par
            |   sum

compare_par ->  'eq' sum
            |   'neq' sum
            |   'lte' sum
            |   'lt' sum
            |   'gte' sum
            |   'gt' sum


sum ->  sum '+' term
    |   sum '-' term
    |   term

term -> term '*' factor
    |   term '/' factor
    |   term '%' factor
    |   factor

factor ->   '+' factor
        |   '-' factor
        |   pow

pow ->  primary '^' 2
    |   primary

primary ->  primary '.' NAME
        |   primary '(' args ')'
        |   primary '(' ')'
        |   atom

args -> expression ',' args
    |   expression

atom -> NAME
    |   'True'
    |   'False'
    |   'None'  
    |   NUMBER
    |   STRING
    |   list

list -> '[' expressions ']'
    |   '[' ']'

expressions ->  expression ',' expressions
            |   expression
```