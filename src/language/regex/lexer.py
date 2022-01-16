from typing import Dict
from .token import Token


class Lexer:
    def __init__(self, pattern: str):
        self.source : str = pattern
        self.symbols: Dict[str: str] = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current: int = 0
        self.length: int = len(self.source)
       
    def __call__(self) -> Token: 
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')
