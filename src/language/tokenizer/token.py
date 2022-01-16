from enum import Enum
from ..regex import Regex

class TokenType(Enum):
    # TODO terminar

    Number = Regex("(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)*")
    Name = Regex("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)+")
    
    # Punctuation
    Semicolon = Regex(";")
    Colon = Regex(":")
    Comma = Regex(",")
    LeftParent = Regex("\(")
    RightParent = Regex("\)")

    # Keywords
    Break = Regex("break")
    Continue = Regex("continue")
    Def_Func = Regex("fn")
    Return = Regex("return")
    If = Regex("if")
    Elif = Regex("elif")
    Else = Regex("else")
    While = Regex("while")
    Equal = Regex("eq")

    # Operadores
    Assign = Regex("=")
    Plus = Regex("\+")
    Minus = Regex("-")
    Mul = Regex("\*")
    Div = Regex("/")
    Mod = Regex("%")
    Pow = Regex("\*\*")
    Not = Regex("!")

class Token:
    @property
    def regex(self) -> Regex:
        return self.type.value

    def __init__(self, token_type: TokenType, lexeme: str, line: int, col: int):
        self.type : TokenType = token_type
        self.lexeme : str = lexeme
        self.line : int = line
        self.col : int = col
    
    