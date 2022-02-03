from .language.compiler import Compiler

program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id \n}} \n number a = 3\n"
Compiler()(program)