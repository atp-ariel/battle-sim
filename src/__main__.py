from .language.compiler import Compiler

program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; };  number a = 3;"
Compiler()(program)