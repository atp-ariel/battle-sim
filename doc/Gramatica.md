# Battle Script grammar

```
bs_file ->  classes statements EOF                                      *
        |   EOF

classes -> class_def NEWLINE classes
        |  class_def                                                *

statements ->   statement NEWLINE statements                           
            |   statement

statement ->    func_def
            |   if_def
            |   while_def
            |   assign
            |   return_stat
            |   'break'                                         *                
            |   'continue'                                      *
            |   expressions


func_def ->     'function' return_type NAME '(' params ')' '->' block       *
            |   'function' return_type NAME '(' ')' '->' block              *

if_def ->   'if' expression '->' block elif_def                             *
        |   'if' expression '->' block else_def                             *
        |   'if' expression '->' block                                      *

elif_def ->     'elif' expression '->' block elif_def                       *
            |   'elif' expression '->' block else_def                       *
            |   'elif' expression '->' block                                *

else_def -> 'else' '->' block                                               *

class_def ->    'class' NAME 'is' NAME '->' block                           *

while_def ->    'while' expression '->' block                               *

return_type ->  "void"
            |   type

type ->     'number' 
        |   NAME

assign ->  type NAME '=' expression                                         *

return_stmt ->  'return' expression                                         *
            |   'return'                                                    *

block ->    NEWLINE "{" statements "}"                                      *

params ->   type NAME ',' params                                           
        |  type NAME                                                        


expressions ->  expression ','  expressions                                 
            |   expression

expression ->   disjunction 'if' disjunction 'else' expression              *
            |   disjunction                                                 *

disjunction ->  conjunction 'or' disjunction                                *
            | conjunction                                                   *

conjunction ->  inversion 'and' conjunction                                 *
            |   inversion                                                   *

inversion ->    'not' inversion                                             *
            |    comparision                                                *


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

pow ->  primary '^' factor              *
    |   primary                         *

primary ->  primary '.' NAME            *
        |   primary '(' args ')'        *
        |   primary '(' ')'             *
        |   atom

atom -> NAME                            *
    |   'True'                          *
    |   'False'                         *
    |   'None'                          *
    |   NUMBER                          *
    |   list                            *

list -> '[' expressions ']'             *
    |   '[' ']'                         *
```