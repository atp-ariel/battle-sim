from .language.compiler import Compiler

#program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; }; & number a = 3;"
#Compiler()(program)

#program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; }; class Archer is LandUnit -> {  constructor(number id, number life_points) -> { number this.id = id; number this.life_points = life_points; }; }; & number a = 3;"
#Compiler()(program)

program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; function number W(number a) -> { if a lte 10 -> { return -1 * a;  } else -> { return a; }; };}; & number a = 3;"
Compiler()(program)