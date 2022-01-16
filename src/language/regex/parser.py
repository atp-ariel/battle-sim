from typing import List
from .token import Token
from .lexer import Lexer

class ParseError(Exception):
    pass

class Parser:
    '''
    Grammar for regex:

    regex = exp $
    Grammar for regex:

    regex = exp $

    exp      = term [|] exp      {push '|'}
            | term
            |                   empty?

    term     = factor term       chain {add \x08}
            | factor

    factor   = primary [*]       star {push '*'}
            | primary [+]       plus {push '+'}
            | primary [?]       optional {push '?'}
            | primary

    primary  = \( exp \)
            | char              literal {push char}
    '''
    def __init__(self, lexer: Lexer):
        self.lexer : Lexer  = lexer
        self.tokens : List[Token] = []
        self.lookahead : Token  = self.lexer()
    
    def consume(self, name: str):
        if self.lookahead.name == name:
            self.lookahead = self.lexer()
        elif self.lookahead.name != name:
            raise ParseError

    def __call__(self) -> List[Token]: 
        self.exp()
        return self.tokens
    
    def exp(self):
        self.term()
        if self.lookahead.name == 'ALT':
            t = self.lookahead
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()
        if self.lookahead.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def factor(self):
        self.primary()
        if self.lookahead.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            self.exp()
            self.consume('RIGHT_PAREN')
        elif self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
            self.consume('CHAR')
