# Battle Script grammar

```
bs_file ->  classes '&' statements EOF     build_program
        |   EOF                       

classes -> class_def ';' classes         build_classes1
        |  class_def ';'                       build_classes2                                         

statements ->   statement ';' statements      build_statements1
            |   statement ';'                      build_statements2

statement ->    func_def
            |   if_def
            |   while_def
            |   decl 
            |   assign 
            |   return_stat 
            |   'break'                            build_breack                             
            |   'continue'                         build_continue             
            |   expression


func_def ->     'function' return_type NAME '(' params ')' '->' "{" statements "}"       build_func_def1
            |   'function' return_type NAME '(' ')' '->' "{" statements "}"              build_func_def2

if_def ->   'if' expression '->' "{" statements "}" elif_def                             build_if_def1
        |   'if' expression '->' "{" statements "}" else_def                             build_if_def2
        |   'if' expression '->' "{" statements "}"                                      build_if_def3

elif_def ->     'elif' expression '->' "{" statements "}" elif_def                       build_elif_def1
            |   'elif' expression '->' "{" statements "}" else_def                       build_elif_def2
            |   'elif' expression '->' "{" statements "}"                                build_elif_def3

else_def -> 'else' '->' "{" statements "}"                                               build_else_def

class_def ->    'class' NAME 'is' NAME '->' '{'  constructor_def ';' functions '}'   build_class_def1
        |       'class' NAME 'is' NAME '->' '{'  constructor_def ';' '}'                     build_class_def2


functions -> func_def ';' functions                     build_functions1
           | func_def ';'                               build_functions2

constructor_def -> 'constructor' '(' params ')' '->' '{' attributes '}'              build_constructor1
             | 'constructor' '(' ')' '->' '{'  attributes '}'                 build_constructor2
             | 'constructor' '(' ')' '->' '{' '}                        build_constructor3


attributes -> attr_def ';'  attributes             build_attributes1
            | attr_def ';'                        build_attributes2

attr_def ->  type 'self' '.' NAME '=' expression           build_attr_def


while_def ->    'while' expression '->' "{" statements "}"              build_while_def

return_type ->  'void'                        build_return_type
            |   type                          build_return_type

type ->   'number'        build_type
      |   'bool'          build_type
      |   'List'          build_type
      |   NAME            build_type

assign -> NAME '=' expression                         build_assign

decl ->  type NAME '=' expression                              build_decl

return_stmt ->  'return' expression                                      build_return1
            |   'return'                                        build_return2

params ->   type NAME ',' params      build_params1
        |  type NAME                  build_params2                                 


expressions ->  expression ','  expressions               build_expressions1
            |   expression                                build_expressions2

expression ->   disjunction 'if' disjunction 'else' expression            build_ternary_expression
            |   disjunction                                                

disjunction ->  conjunction 'or' disjunction                                build_disjunction
            | conjunction                                                   

conjunction ->  inversion 'and' conjunction                                 build_conjuction
            |   inversion                                                   

inversion ->    'not' inversion                                             build_inversion
            |    comparision                                                


comparision ->  sum 'eq' sum                       build_comparision
            |   sum 'neq' sum                      build_comparision 
            |   sum 'lte' sum                      build_comparision 
            |   sum 'lt' sum                       build_comparision 
            |   sum 'gte' sum                      build_comparision
            |   sum 'gt' sum                       build_comparision
            |   sum


sum ->  sum '+' term                            build_aritmetic_expression
    |   sum '-' term                            build_aritmetic_expression
    |   term 

term -> term '*' factor                         build_aritmetic_expression
    |   term '/' factor                         build_aritmetic_expression
    |   term '%' factor                         build_aritmetic_expression
    |   factor

factor ->   '+' factor
        |   '-' factor
        |   pow

pow ->  primary '^' factor              build_aritmetic_expression
    |   primary

primary ->  primary '.' NAME            build_primary1
        |   primary '(' expressions ')'        build_primary2
        |   primary '(' ')'             build_primary3
        |   atom
        | '(' expression ')'            build_pexpression

atom -> NAME                            build_Variable
    |   'True'                          build_Bool
    |   'False'                         build_Bool
    |   'None'                          build_None
    |   NUMBER                          build_Number
    |   list

list -> '[' expressions ']'             build_list1
    |   '[' ']'                         build_list2
```
