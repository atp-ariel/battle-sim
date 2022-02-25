from enum import Enum
from ..regex import Regex


class TokenType(Enum):
    Number = (Regex(
        "-?((0|1|2|3|4|5|6|7|8|9)+(\.(0|1|2|3|4|5|6|7|8|9)+)?)"), "NUMBER")
    Name = (Regex("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_)+"), "NAME")
    Arrow = (Regex("->"), "->")
    Comma = (Regex(","), ",")
    LeftParent = (Regex("\("), "(")
    LeftCurly = (Regex("{"), "{")
    RightCurly = (Regex("}"), "}")
    RightParent = (Regex("\)"), ")")
    Break = (Regex("break"), "break")
    Continue = (Regex("continue"), "continue")
    Def_Func = (Regex("function"), "function")
    Return = (Regex("return"), 'return')
    If = (Regex("if"), 'if')
    Elif = (Regex("elif"), "elif")
    Else = (Regex("else"), "else")
    Class = (Regex("class"), "class")
    While = (Regex("while"), "while")
    Equal = (Regex("eq"), "eq")
    Neq = (Regex("neq"), "neq")
    Lte = (Regex("lte"), "lte")
    Gte = (Regex("gte"), "gte")
    Gt = (Regex("gt"), "gt")
    Lt = (Regex("lt"), "lt")
    Is = (Regex("is"), "is")
    TNumber = (Regex("number"), "number")
    Assign = (Regex("="), "=")
    Plus = (Regex("\+"), "+")
    Minus = (Regex("-"), "-")
    Mul = (Regex("\*"), "*")
    Div = (Regex("/"), "/")
    Mod = (Regex("%"), "%")
    Pow = (Regex("^"), "^")
    Not = (Regex("not"), "not")
    Or = (Regex("or"), "or")
    And = (Regex("and"), "and")
    Dot = (Regex("\."), ".")
    Semicolon = (Regex(";"), ";")
    LeftBracket = (Regex("["), "[")
    RightBracket = (Regex("]"), "]")
    true = (Regex("True"), "True")
    false = (Regex("False"), "False")
    none = (Regex("None"), "None")
    void = (Regex("void"), "void")
    Bool = (Regex("bool"), "bool")
    Self = (Regex("self"), "self")
    Constructor = (Regex("constructor"), "constructor")
    OAnd = (Regex("&"), "&")
    EOF = (Regex("EOF"), "EOF")
    List = (Regex("List"), "List")


class TokenDefinition:
    def __init__(self, ttype: TokenType, precendence: int):
        self.type: TokenType = ttype
        self.precendece: int = precendence

    def __hash__(self):
        return self.precendece.__hash__() + self.type.value[0].nfa.start.name.__hash__()


class Token:
    @property
    def regex(self) -> Regex:
        return self.type.value[0]

    @property
    def name(self) -> str:
        return self.type.value[1]

    def __init__(self, token_type: TokenType, lexeme: str, start: int, end: int):
        self.type: TokenType = token_type
        self.lexeme: str = lexeme
        self.start: int = start
        self.end: int = end
