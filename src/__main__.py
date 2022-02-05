from .language.compiler import Compiler

# program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; }; & List a = [ 1, 2, 3, [1,2] ];"
# Compiler()(program)

# program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; }; class Archer is LandUnit -> {  constructor(number id, number life_points) -> { number this.id = id; number this.life_points = life_points; }; }; & number a = 3;"
# Compiler()(program)

# program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id; }; function number W(number a) -> { return a + 2; };}; & number a = 3; while 5 eq 1 -> { a = -1 * a;  };"
# Compiler()(program)

# program = "class Soldier is LandUnit -> {  constructor(number id) -> { number this.id = id + 3 * 5^-2; }; function number W(number a) -> { if a lt 0 and a eq 0-> { return -1 * a;  } elif a gt 1 -> {return 4;} else -> { return a; }; };}; class Archer is LandUnit -> {  constructor(number id, number life_points) -> { number this.id = id; number this.life_points = life_points; }; }; & Soldier b = Soldier(1); Soldier bOne = Soldier(3); Archer a = Archer(1, 10); if a eq None -> { a = a + 1; }; a = [1,2,3, [1,2,3,4] ];"
# Compiler()(program)

program = "class Soldier is LandUnit -> { constructor(number id, number attack) -> { number this.id = id; number this.attack = attack; }; }; & function number W(number a) -> { while True -> {a = a + 1;}; return a;};"
Compiler()(program)