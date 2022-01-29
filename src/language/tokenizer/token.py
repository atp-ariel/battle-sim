from dataclasses import dataclass
from enum import Enum
from typing import Generator
from ..regex import Regex

class TokenType(Enum):
    Number = Regex("(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*(\.)*(0|1|2|3|4|5|6|7|8|9)*")
    Name = Regex("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)+")
    Arrow = Regex("->")
    Comma = Regex(",")
    LeftParent = Regex("\(")
    LeftCurly = Regex("{")
    RightCurly = Regex("}")
    RightParent = Regex("\)")
    Break = Regex("break")
    Continue = Regex("continue")
    Def_Func = Regex("function")
    Return = Regex("return")
    If = Regex("if")
    Elif = Regex("elif")
    Else = Regex("else")
    Class = Regex("class")
    While = Regex("while")
    Equal = Regex("eq")
    Neq = Regex("neq")
    Lte = Regex("lte")
    Gte = Regex("gte")
    Gt = Regex("gt")
    Lt = Regex("lt")
    Is = Regex("is")
    TNumber = Regex("number")
    Assign = Regex("=")
    Plus = Regex("\+")
    Minus = Regex("-")
    Mul = Regex("\*")
    Div = Regex("/")
    Mod = Regex("%")
    Pow = Regex("^")
    Not = Regex("not")
    Or = Regex("or")
    And = Regex("and")
    Dot = Regex("\.")
    Newline = Regex("\n")
    LeftBracket = Regex("[")
    RightBracket = Regex("]")
    true = Regex("True")
    false = Regex("False")
    none = Regex("None")
    void = Regex("void")

class TokenDefinition:
    def __init__(self, ttype: TokenType, precendence: int):
        self.type : TokenType = ttype
        self.precendece : int = precendence

    def __hash__(self):
        return self.precendece.__hash__() + self.type.value.nfa.start.name.__hash__()

class Token:
    @property
    def regex(self) -> Regex:
        return self.type.value

    def __init__(self, token_type: TokenType, lexeme: str, start: int, end: int):
        self.type : TokenType = token_type
        self.lexeme : str = lexeme
        self.start : int = start
        self.end : int = end
    
    